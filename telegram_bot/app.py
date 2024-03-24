import json
import boto3
import logging
import os
import requests
import urllib.request
import re

import config as cfg
import user as usr
import record as rec

logger = logging.getLogger(__name__)

TABLE_NAME = 'feedings'

if os.environ.get('ENV') is None:
    ENV = cfg.ENV
else:
    ENV = os.environ['ENV']


def create_user(data: dict):
    """
    Creates new TelegramUser instance, from data message.

    Params:
        data: dict, data from event / Telegram API Webhook

    Returns:
        user: TelegramUser instance
    """
    user = usr.TelegramUser(id=data['from']['id'],
                            username=data['from']['username'],
                            first_name=data['from']['first_name'],
                            is_bot=data['from']['is_bot'],
                            chat_id=data['chat']['id'],
                            message=data['text']
                            )
    return user


def reply_user(chat_id: int, reply_message: str):
    """
    Prepares bot token, api endpoint, then performs a POST request to Telegram API.

    Params:
        chat_id:       int, chat_id of user
        reply_message: str, text message to reply to the user

    Returns:
        response:  json, if POST request is performed
        False:     bool, if telegram bot token is None. i.e. not retrieved.
    """
    token = get_bot_credentials()
    if token is None:
        logger.error(f'Error. Invalid Token={token}')
        return False

    reply_url = get_bot_url(token)

    params = {'chat_id': chat_id, 'text': reply_message}
    response = requests.post(reply_url, json=params)

    return response.json()


def get_bot_url(credentials):
    """
    Construct Telegram API URL based on Bot credentials. URL format: https://api.telegram.org/bot<token>/METHOD_NAME

    Params:
        credentials: str, Telegram Bot private token

    Returns:
        url: str, Telegram API endpoint
    """
    url = f'{cfg.BOT_BASE_URL}{credentials}/{cfg.BOT_METHOD}'
    return url


def get_bot_credentials(token_name=cfg.BOT_TOKEN_NAME):
    """
    Get secret Telegram Bot Token/Credential from AWS Parameter Store.
    Uses AWS Parameters and Secrets Lambda Extension, that allows caching.

    Params:
        token_name: str, name of the token, from config.py

    Returns:
        secret: str, secret token from AWS Parameter Store
        None:   None, if token_name is not correct
    """
    secret_ext_endpoint = (f'http://localhost:{cfg.SECRET_EXT_PORT}/systemsmanager/parameters/'
                           f'get?name={cfg.TOKEN_PARAM_PATH}&withDecryption=true')
    request_ssm = urllib.request.Request(secret_ext_endpoint)
    request_ssm.add_header('X-Aws-Parameters-Secrets-Token', os.environ.get('AWS_SESSION_TOKEN'))
    resp = urllib.request.urlopen(request_ssm).read()

    secret_name = json.loads(resp)['Parameter']['Name']
    secret = json.loads(resp)['Parameter']['Value']

    if secret_name == token_name:
        return secret
    return None


def load_amount_ml(text):
    """
    Reads amount(millilitres) from text. E.g. for "12.30pm 200ml" it should return value 200.
    Params:
        text: str, text message content

    Returns:
        amount: int, the parsed amount from the text message. only the last matching amount is returned
        -1    : int, if the amount is not found
    """
    pattern = re.compile(r'^.*\s(\d+)ml.*$')
    m_ = pattern.match(text)
    if m_ is not None:
        amount = m_.group(1)
        return int(amount)
    return -1


def read_action(message, amt):
    """
    Gives action based on params.

    Params:
        amt: int, the amount of milk in units e.g. millimetres

    Returns:
        Action: str, the next action to take for Lambda handler
    """
    msg = message.strip().upper()
    if amt > 0:
        return 'RECORD'
    elif msg == 'TODAY':
        return 'TODAY'
    elif msg == 'YESTERDAY':
        return 'YESTERDAY'
    else:
        return 'UNKNOWN'


def lambda_handler(event: dict, context: object):
    """
    Lambda handler that receives events from API Gateway. Performs action for users, and responds back to API Gateway.

    Params:
    event: dict, required
        API Gateway Lambda Proxy Input Format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns:
        API Gateway Lambda Proxy Output Format: dict
        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    logger.info(f"Running Environment={ENV}")

    try:
        data = json.loads(event['body'])['message']
    except Exception as e:
        logger.exception(f"An unexpected error occurs: {e} ")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. An unexpected error occurs."})
        }

    user = create_user(data)

    if user.validate_self():
        logger.info(f"Validated user={user.first_name}, message={user.message}")
        amt = load_amount_ml(user.message)
        print(f'amount found is {amt}')

        action = read_action(user.message, amt)
        print(f'action is {action}')

        if action != 'UNKNOWN':
            print(f'TABLE_NAME={TABLE_NAME}')
            records = rec.Records(boto3.resource('dynamodb', region_name='ap-southeast-2'))
            records.init_table(TABLE_NAME)

            if action == 'RECORD' and ENV == 'PROD':
                records.add_record(category="MILK", amount=amt, message=user.message, author=user.first_name)
                reply_user(user.chat_id, "Recorded")

            elif action == 'TODAY' and ENV == 'PROD':
                print('Staring TODAY')
                date_ = rec.get_date_action(action)
                print(f'rec.get_date_action(action)={date_}')
                if date_ is not None:
                    results = records.query_records(date_)
                    total_amount = 0
                    consolidated_message = ''
                    print(f'results={results}')
                    for result in results:
                        total_amount += result['amount']
                        consolidated_message += (result['text'] + '\n')
                    print(f'total_amount={total_amount}, consolidated_message={consolidated_message}')
                    output = f'Total drank = {total_amount}ml\n{consolidated_message}'
                    reply_user(user.chat_id, output)

            elif ENV == 'PROD':
                reply_user(user.chat_id, "Ok")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Ok"})
    }

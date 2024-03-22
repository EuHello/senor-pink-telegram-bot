import json
import logging
import os
import requests
import urllib.request

import config as cfg
import user as usr

logger = logging.getLogger()
logger.setLevel('INFO')

APP = 'BOT_APP: '

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
                        username= data['from']['username'],
                        first_name = data['from']['first_name'],
                        is_bot=data['from']['is_bot'],
                        chat_id=data['chat']['id'],
                        message=data['text'],
                        )
    return user


def validate_user(user: usr.TelegramUser, allowed_users=cfg.allowed_ids):
    """
    Validates TelegramUser instance. Checks whether lambda handler should act on the user.

    Params:
        user: TelegramUser instance

    Returns:
        True:  bool, user is validated and in allowed list
        False: bool, if otherwise
    """
    if not user.validate_self():
        return False
    if user.is_bot or user.chat_id < 0:
        return False
    if user.id in allowed_users:
        return True
    return False


def parse_text():
    return True


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
        logger.error(f'{APP}Error. Invalid Token={token}')
        return False

    reply_url = get_bot_url(token)

    params = {'chat_id': chat_id, 'text': reply_message}
    response = requests.post(reply_url, json=params)

    return response.json()


def get_bot_url(credentials):
    """
    Construct Telegram API URL based on Bot credentials.
    URL format: https://api.telegram.org/bot<token>/METHOD_NAME

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

    try:
        ret = json.loads(event['body'])['message']
    except json.JSONDecodeError as e:
        logger.exception(f"{APP}Error parsing json: {e}")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error parsing json."})
        }
    except KeyError as e:
        logger.exception(f"{APP}Error. Key not found in json: {e}")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. Key not found in json."})
        }
    except Exception as e:
        logger.exception(f"{APP}Error. An unexpected error occurs: {e} ")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. An unexpected error occurs."})
        }

    data = json.loads(event['body'])['message']
    user = create_user(data)

    if validate_user(user):
        logger.info(f"{APP}Validated user={user.first_name}, message={user.message}")
        if ENV == 'PROD':
            reply_user(user.chat_id, "Ok")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Ok"})
    }

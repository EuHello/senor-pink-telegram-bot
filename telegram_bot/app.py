import json
import logging
import os
import requests
import urllib.request

from .config import allowed_ids, BOT_BASE_URL, BOT_METHOD, TOKEN_PARAM_PATH, SECRET_EXT_PORT, BOT_TOKEN
from .user import TelegramUser

logger = logging.getLogger()
logger.setLevel('INFO')

BOT_APP = 'BOT_APP: '


def create_user(data: dict):
    """
    Creates new TelegramUser instance, from data message.

    Params:
        data: dict, data from event / Telegram API Webhook

    Returns:
        user: TelegramUser instance
    """
    user = TelegramUser(user_id=data['from']['id'],
                        username = data['from']['username'],
                        first_name = data['from']['first_name'],
                        is_bot=data['from']['is_bot'])
    user.set_chat_id(data['chat']['id'])
    user.set_message(data['text'])
    return user


def validate_user(user: TelegramUser, allowed_users=allowed_ids):
    """
    Validates TelegramUser instance. Checks whether lambda handler should act on the user.

    Params:
        user: TelegramUser instance

    Returns:
        True:  bool, if user is valid
        False: bool, otherwise
    """
    print(allowed_users)
    if user.is_bot:
        return False
    if user.chat_id < 0:
        return False
    if user.uid in allowed_users:
        return True
    return False


def parse_text():
    return True


def reply_user(chat_id: int, reply_message: str):
    """
    Wrapper function that responds a message to TelegramUser.

    Params:
        chat_id:       int, chat_id of the user
        reply_message: str, message to reply to the user

    Returns:
        True:  bool, if no issue found
        False: bool, if telegram bot token is None. i.e. not retrieved.
    """
    token = get_bot_credentials()
    if token is None:
        logger.info(f"{BOT_APP}Invalid Token")
        return False
    reply_url = get_bot_url(token)
    response = chat_user(chat_id, reply_message, reply_url)
    return True


def chat_user(chat_id: int, reply_text: str, chat_url):
    """
    Performs a POST request to Telegram API.

    Params:
        chat_id:    int, chat_id of the user
        reply_text: str, text message to reply to the user
        chat_url:   str, Telegram API endpoint

    Returns:
        json:     json response from Telegram API
    """
    params = {"chat_id": chat_id, "text": reply_text}
    response = requests.post(chat_url, json=params)
    return response.json()


def get_bot_url(credentials):
    """
    Construct Telegram API URL based on Bot's credentials.

    Params:
        credentials: str, Telegram Bot's private token

    Returns:
        url: str, Telegram API endpoint
    """
    url = f'{BOT_BASE_URL}{credentials}/{BOT_METHOD}'
    return url


def get_bot_credentials(token_name=BOT_TOKEN):
    """
    Get secret Telegram Bot Token/Credential from AWS Parameter Store.
    Uses AWS Parameters and Secrets Lambda Extension, that allows caching.

    Params:
        token_name: str, name of the token, from config.py

    Returns:
        secret: str, secret token from AWS Parameter Store
        None:   None, if token_name is not correct
    """
    secret_ext_endpoint = (f'http://localhost:{SECRET_EXT_PORT}/systemsmanager/parameters/'
                           f'get?name={TOKEN_PARAM_PATH}&withDecryption=true')
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
        logger.error(f"{BOT_APP}Error parsing json: {e}")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error parsing json."})
        }
    except KeyError as e:
        logger.error(f"{BOT_APP}Error. Key not found in json: {e}")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. Key not found in json."})
        }
    except Exception as e:
        logger.error(f"{BOT_APP}Error. An unexpected error occurs: {e} ")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. An unexpected error occurs."})
        }

    data = json.loads(event['body'])['message']
    user = create_user(data)

    if validate_user(user):
        logger.info(f"{BOT_APP}Valid user={user.first_name}, message={user.message}")
        reply_user(user.chat_id, "Ok")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Ok"})
    }

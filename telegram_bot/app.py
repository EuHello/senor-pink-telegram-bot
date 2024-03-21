import json
import logging
import os
import requests
import urllib.request

from config import valid_user_ids, BOT_BASE_URL, BOT_METHOD, TOKEN_PARAM_PATH, SECRET_EXT_PORT, BOT_TOKEN
from user import TelegramUser

logger = logging.getLogger()
logger.setLevel('INFO')

BOT_APP = 'BOT_APP: '


def create_user(message_body: dict):
    user = TelegramUser(user_id=message_body['from']['id'],
                        username = message_body['from']['username'],
                        first_name = message_body['from']['first_name'],
                        is_bot=message_body['from']['is_bot'])
    user.add_chat_id(message_body['chat']['id'])
    user.add_message(message_body['text'])
    return user


def validate_user(user: TelegramUser):
    if user.is_bot:
        return False
    if user.chat_id < 0:
        return False
    if user.uid in valid_user_ids:
        return True
    return False


def parse_text():
    return True


def reply_user(chat_id: int, message: str):
    token = get_bot_credentials()
    if token is None:
        logger.info(f"{BOT_APP}Invalid Token")
        return False
    reply_url = get_bot_url(token)
    response = chat_user(chat_id, message, reply_url)
    return True


def chat_user(chat_id: int, text: str, chat_url):
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(chat_url, json=params)
    return response.json()


def get_bot_url(credentials):
    url = f'{BOT_BASE_URL}{credentials}/{BOT_METHOD}'
    return url


def get_bot_credentials(bot_name=BOT_TOKEN):
    secret_ext_endpoint = (f'http://localhost:{SECRET_EXT_PORT}/systemsmanager/parameters/'
                           f'get?name={TOKEN_PARAM_PATH}&withDecryption=true')
    request_ssm = urllib.request.Request(secret_ext_endpoint)
    request_ssm.add_header('X-Aws-Parameters-Secrets-Token', os.environ.get('AWS_SESSION_TOKEN'))
    resp = urllib.request.urlopen(request_ssm).read()

    secret_name = json.loads(resp)['Parameter']['Name']
    secret = json.loads(resp)['Parameter']['Value']

    if secret_name == bot_name:
        return secret

    return None


def lambda_handler(event, context):
    """
    Lambda function that reads text and replies user after validation

    Params
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes
        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # logger.debug(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    # logger.debug(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])

    try:
        body = json.loads(event['body'])
        message_body = body['message']
    except json.JSONDecodeError as e:
        logger.error(f"{BOT_APP}Error parsing json: {e}")
    except KeyError as e:
        logger.error(f"{BOT_APP}Key not found in json: {e}")
    except Exception as e:
        logger.error(f"{BOT_APP}An unexpected error occurs: {e} ")

    user = create_user(message_body)

    if validate_user(user):
        logger.info(f"{BOT_APP}Valid user={user.first_name}, message={user.message}")
        reply_user(user.chat_id, "Ok")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Ok"
        }),
    }

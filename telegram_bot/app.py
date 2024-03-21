import json
import logging
import os
import requests
import urllib.request

from config import valid_user_ids, valid_usernames, BOT_BASE_URL, BOT_METHOD, TOKEN_PARAM_PATH, SECRET_EXT_PORT, BOT_TOKEN

logger = logging.getLogger()
logger.setLevel("INFO")


def validate_user(username: str, userid: int, bot_status: bool):
    if bot_status:
        return False
    if userid in valid_user_ids:
        return True
    if username in valid_usernames:
        return True
    return False


def parse_text():
    return True


def reply_user(chat_id: int, text: str):
    token = get_bot_credentials()
    if token is None:
        logger.info("Invalid Token")
        return False
    reply_url = get_bot_url(token)
    response = chat_user(chat_id, text, reply_url)
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

    logger.debug(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    logger.debug(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])

    try:
        body = json.loads(event['body'])
        message_body = body['message']
    except json.JSONDecodeError as e:
        logger.error("Error parsing json: ", e)
    except KeyError as e:
        logger.error("Key not found in json: ", e)
    except Exception as e:
        logger.error("An unexpected error occurs ", e)

    message_text = message_body['text']
    chat_id = message_body['chat']['id']
    username = message_body['from']['username']
    user = message_body['from']['first_name']
    userid = message_body['from']['id']
    is_bot = message_body['from']['is_bot']

    if validate_user(username, userid, is_bot):
        reply_user(chat_id, "Ok")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Ok"
        }),
    }

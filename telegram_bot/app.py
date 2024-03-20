import json
import logging
import os
import requests

from config import valid_user_ids, valid_usernames, REPLY_URL

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
    url = REPLY_URL
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=params)
    return response.json()


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
        response = reply_user(chat_id, "Yes im working")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Ok"
        }),
    }

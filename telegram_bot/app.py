import json
import logging
import os
# import requests


logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
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

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    logger.debug(os.environ['AWS_LAMBDA_LOG_GROUP_NAME'])
    logger.debug(os.environ['AWS_LAMBDA_LOG_STREAM_NAME'])
    logger.info("EVENT")
    logger.info(event)
    logger.info("EVENT-body")
    logger.info(event['body'])
    logger.info("EVENT-body-message")
    logger.info(event['body']['message'])
    logger.info("EVENT-body-message-text")
    logger.info(event['body']['message']['text'])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

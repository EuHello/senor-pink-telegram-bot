import json
import boto3
import logging
import os
import re

import config as cfg
import user as usr
import record as rec
import reply as rep
import controller as ctr

logger = logging.getLogger(__name__)

TABLE_NAME = 'feedings'

if os.environ.get('ENV') is None:
    ENV = cfg.ENV
else:
    ENV = os.environ['ENV']


def create_user(data: dict):
    """Creates new TelegramUser instance, from data message.

    Params:
    data: dict, data from event / Telegram API Webhook
    """
    user = usr.TelegramUser(id=data['from']['id'],
                            first_name=data['from']['first_name'],
                            is_bot=data['from']['is_bot'],
                            chat_id=data['chat']['id'],
                            message=data['text']
                            )
    return user


def load_amount_ml(text):
    """Reads amount (millilitres) from text. E.g. for "12.30pm 200ml" it should return value 200.
    Params:
    text: str, text message content

    Returns:
    amount: int, the parsed amount from the text message. only the last matching amount is returned
    -1    : int, if the amount is not found
    """
    pattern = re.compile(r'^.*\s(\d+)ML.*$')
    m_ = pattern.match(text.upper())
    if m_ is not None:
        amount = m_.group(1)
        return int(amount)
    return 0


def read_message(message):
    """Returns action command to Lambda handler from text message input.

    Params:
    message: str, text message to be parsed

    Returns:
    action: str, the next action to take for Lambda handler. e.g. RECORD
    """
    msg = message.strip().upper()
    if msg == 'TODAY':
        return 'TODAY'
    elif msg == 'YESTERDAY':
        return 'YESTERDAY'
    else:
        return 'RECORD'


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
    logger.info(f"Init lambda_handler = {ENV}")

    try:
        data = json.loads(event['body'])['message']
    except Exception as e:
        logger.exception(f"An unexpected error occurs: {e} ")
        return {
            'statusCode': 400,
            "body": json.dumps({"message": "Error. An unexpected error occurs."})
        }

    logger.info(f"New chat, data={data}")
    user = create_user(data)
    logger.info(f"New chat, user={user.first_name}, id={user.chat_id}, message={user.message}")

    if user.validate_self():
        action = read_message(user.message)
        logger.info(f"Validated user={user.first_name}, action={action}, message={user.message}")

        reply = rep.Reply(cfg.BOT_TOKEN_NAME)
        control = ctr.Controller()

        records = rec.Records(boto3.resource('dynamodb', region_name='ap-southeast-2'))
        records.init_table(TABLE_NAME)

        if action == 'RECORD':
            amt = load_amount_ml(user.message)
            records.add_record(category="MILK", amount=amt, message=user.message, author=user.first_name)
            if ENV == 'PROD':
                reply.send_text(user.chat_id, "Recorded")

        elif action == 'TODAY' or action == 'YESTERDAY':
            date_key = control.query_key(action)
            logger.info(f'Querying for date key ={date_key}')
            results = records.query_records(date_key)
            logger.info(f'Query results={results}')
            total_amount = 0
            consolidated_message = ''
            if len(results) == 0:
                reply_text = 'No records found'
            else:
                for result in results:
                    total_amount += result['amount']
                    consolidated_message += (result['text'] + '\n')
                reply_text = f'Total drank = {total_amount}ml\n{consolidated_message}'
            if ENV == 'PROD':
                reply.send_text(user.chat_id, reply_text)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Ok"})
    }

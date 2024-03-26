import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

import controller as ctr

logger = logging.getLogger(__name__)


class Records:
    def __init__(self, dyn_resource):
        """Init class Records, input type is boto3.resource

        Docs:
        https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html
        https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/dynamodb#code-examples
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def init_table(self, table_name: str):
        """Init DynamoDB table, from table name"""
        self.table = self.dyn_resource.Table(table_name)
        logger.info(f'Init table. table_name = {table_name}')

    def query_records(self, date):
        date = str(date)
        logger.info(f'Querying records for date={date}')
        try:
            response = self.table.query(KeyConditionExpression=Key("date").eq(date))
        except ClientError as e:
            logger.error(
                f"Error querying records. Table={self.table.name}.\n"
                f"date={date}\n"
                f"Error Code={e.response['Error']['Code']}\n"
                f"Error={e.response['Error']['Message']}"
            )
            raise
        else:
            return response["Items"]

    def add_record(self, category: str, amount: int, message: str, author: str):
        """PUTS record to DynamoDB. Composite primary key consists date and timestamp (string type)

        Params:
        category: str, category of record. e.g. milk
        amount: int, value of measurement e.g. 100 ml
        message: str, text message from the user
        author: str, name of user
        """
        control = ctr.Controller()
        date, timestamp = control.keys_put_record()
        logger.info(f'Adding a new record. category={category}, amount={amount}, message={message}, author={author}')
        try:
            self.table.put_item(
                Item={
                    'date': date,
                    'timestamp': timestamp,
                    'category': category,
                    'amount': amount,
                    'text': message,
                    'author': author
                }
            )
        except ClientError as e:
            (logger.error(
                f"Error adding a record. Table={self.table.name}.\n"
                f"date={date}\n"
                f"Error Code={e.response['Error']['Code']}\n"
                f"Error={e.response['Error']['Message']}"
            ))
            raise

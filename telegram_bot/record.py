import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from botocore.exceptions import ClientError

APP = 'BOT_APP: '


def get_date_timestamp():
    """
    Provides local date, based on specified timezone, not the server timezone.
    Params: n/a

    Returns:
        date: datetime date, this comes in format YYYY-MM-DD.
        time: datetime time, this comes in format HH:MM:SS.ssssss
    """
    today = datetime.now()
    user_dt = today.astimezone(ZoneInfo('Asia/Singapore'))
    return str(user_dt.date()), str(user_dt.time())


class Records:
    def __init__(self, dyn_resource):
        """
        Init DynamoDB connection

        Params:
            dyn_resource: boto3.resource

        """
        self.dyn_resource = dyn_resource
        self.table = None

    def init_table(self, table_name: str):
        """
        Init DynamoDB table

        Params:
            table_name: str, name of DB table
        """
        self.table = self.dyn_resource.Table(table_name)

    def add_record(self, category: str, amount: int, message: str, author: str):
        '''
        PUTS record to DynamoDB. Composite primary key consists of date and timestamp, both generated by a function.

        Params:
            category: str, category of record. e.g. milk
            amount: int, value of measurement e.g. 100 ml
            message: str, text message from the user
            author: str, name of user
        '''
        date, timestamp = get_date_timestamp()
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
            logging.error(
                f"{APP}Error adding a record. Table={self.table.name}.\n"
                f"date={date}\n"
                f"Error Code={e.response['Error']['Code']}\n"
                f"Error={e.response['Error']['Message']}"
            )
            raise

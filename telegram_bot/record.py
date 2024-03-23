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
        self.dyn_resource = dyn_resource
        self.table = None

    def init_table(self, table_name:str):
        self.table = self.dyn_resource.Table(table_name)

    def add_record(self, type: str, amount: int, message: str, author: str):
        date, timestamp = get_date_timestamp()
        try:
            self.table.put_item(
                Item={
                    'date': date,
                    'timestamp': timestamp,
                    'type': type,
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

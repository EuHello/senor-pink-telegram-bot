import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


class Controller:
    """From command, return primary keys to retrieve data from DB"""
    def __init__(self):
        self.user_dt = None
        self.yesterday = ''

    def generate_user_datetime(self):
        """Generate local date and timestamp, from specified timezone, not server timezone."""
        today = datetime.now()
        self.user_dt = today.astimezone(ZoneInfo('Asia/Singapore'))
        return self.user_dt

    def create_pkey_date_now(self):
        """Returns primary key - date, as a string. Format YYYY-MM-DD"""
        self.generate_user_datetime()
        return str(self.user_dt.date())

    def create_pkeys_date_timestamp_now(self):
        """Returns primary keys - both date and timestamp as strings.

        Returns:
        date:      string. Format YYYY-MM-DD
        timestamp: string. Format HH:MM:SS.ssssss"""
        self.generate_user_datetime()
        return str(self.user_dt.date()), str(self.user_dt.time())

    def create_pkey_date_yesterday(self):
        """Returns primary key - date for Yesterday, as a string. Format YYYY-MM-DD"""
        self.generate_user_datetime()
        delta = timedelta(days=1)
        return str(self.user_dt.date() - delta)

    def get_pkey_query(self, command: str):
        """Returns primary key(date) depending on input Command.

        Params:
        command: str, fixed command phrase like TODAY or YESTERDAY

        Returns:
        date: datetime date, primary key for DB
        """
        cmd = command.upper().strip()
        if cmd == 'TODAY':
            return self.create_pkey_date_now()
        elif cmd == 'YESTERDAY':
            return self.create_pkey_date_yesterday()
        else:
            return None

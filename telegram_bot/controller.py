import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


class Controller:
    """Methods to produce primary keys, for DB activities"""
    def __init__(self):
        self.user_dt = None
        self.yesterday = ''

    def gen_user_dt(self):
        """Generate local date and timestamp, from specified timezone, not server timezone"""
        today = datetime.now()
        self.user_dt = today.astimezone(ZoneInfo('Asia/Singapore'))
        return self.user_dt

    def key_today(self):
        """Return primary key - date, as a string. Format YYYY-MM-DD"""
        self.gen_user_dt()
        return str(self.user_dt.date())

    def keys_put_record(self):
        """Return primary keys - both date and timestamp as strings

        Returns:
        date:      string. Format YYYY-MM-DD
        timestamp: string. Format HH:MM:SS.ssssss"""
        self.gen_user_dt()
        return str(self.user_dt.date()), str(self.user_dt.time())

    def key_yesterday(self):
        """Return primary key - date for Yesterday, as a string. Format YYYY-MM-DD"""
        self.gen_user_dt()
        delta = timedelta(days=1)
        return str(self.user_dt.date() - delta)

    def query_key(self, command: str):
        """Return primary key(date) depending on input Command

        Params:
        command: str, fixed command phrase like TODAY or YESTERDAY

        Returns:
        date: datetime date, primary key for DB
        """
        cmd = command.upper().strip()
        if cmd == 'TODAY':
            return self.key_today()
        elif cmd == 'YESTERDAY':
            return self.key_yesterday()
        else:
            return None

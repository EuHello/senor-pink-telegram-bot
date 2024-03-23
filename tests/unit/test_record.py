import pytest
from datetime import datetime, timedelta

from . import context
from telegram_bot import record


class TestGenerateDateTimestamp:
    def test_object_type(self):
        date, timestamp = record.generate_date_timestamp()
        assert type(date) is type(datetime.now().date())
        assert type(timestamp) is type(datetime.now().time())


class TestGetDateAction:
    def test_action_today(self):
        date_, _ = record.generate_date_timestamp()
        assert record.get_date_action("TODAY") == date_
        assert record.get_date_action("today") == date_

    def test_action_yesterday(self):
        date_, _ = record.generate_date_timestamp()
        assert record.get_date_action("YESTERDAY") == (date_ - timedelta(days=1))
        assert record.get_date_action("yesterday") == (date_ - timedelta(days=1))

    def test_unknown_action(self):
        assert record.get_date_action("Hello") is None

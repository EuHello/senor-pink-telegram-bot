import pytest

from . import context
from telegram_bot import record


class TestGetDateTimestamp:
    def test_date_timestamp_type(self):
        date, timestamp = record.get_date_timestamp()
        assert isinstance(date, str)
        assert isinstance(timestamp, str)

    def test_date_format(self):
        date, timestamp = record.get_date_timestamp()
        sample_date = "2024-03-24"
        assert len(date) == len(sample_date)

    def test_time_format(self):
        date, timestamp = record.get_date_timestamp()
        sample_time = "HH:MM:SS.ssssss"
        assert len(timestamp) == len(sample_time)

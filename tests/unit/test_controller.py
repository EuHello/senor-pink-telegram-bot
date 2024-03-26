import pytest
from datetime import datetime, timedelta

from . import context
from telegram_bot import controller as ctr


class TestController:
    @pytest.fixture
    def generate_controller(self):
        return ctr.Controller()

    def test_generate_user_datetime(self, generate_controller):
        control = generate_controller
        date = control.gen_user_dt()
        assert type(date) is type(datetime.now())

    def test_create_pkey_date_now(self, generate_controller):
        control = generate_controller
        date = control.key_today()
        assert isinstance(date, str)

    def test_create_pkeys_date_timestamp_now(self, generate_controller):
        control = generate_controller
        date, timestamp = control.keys_put_record()
        assert isinstance(date, str)
        assert isinstance(timestamp, str)
        assert len(date) is len(str(datetime.now().date()))
        assert len(timestamp) is len(str(datetime.now().time()))

    def test_create_pkey_date_yesterday(self, generate_controller):
        control = generate_controller
        date = control.key_today()
        assert isinstance(date, str)


class TestGetPKeyQuery:
    @pytest.fixture
    def generate_controller(self):
        return ctr.Controller()

    def test_action_today(self, generate_controller):
        control = generate_controller
        date = control.key_today()

        assert control.query_key("TODAY") == date
        assert control.query_key("today") == date

    def test_action_yesterday(self, generate_controller):
        control = generate_controller
        date = control.gen_user_dt()
        assert control.query_key("YESTERDAY") == str(date.date() - timedelta(days=1))
        assert control.query_key("yesterday") == str(date.date() - timedelta(days=1))

    def test_unknown_action(self, generate_controller):
        control = generate_controller
        assert control.query_key("Hello") is None

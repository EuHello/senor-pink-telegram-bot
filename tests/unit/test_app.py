import pytest

from . import context
from telegram_bot import app


class TestCreateUser:

    @pytest.fixture
    def generate_data(self):
        return {'from': {'id': 12345678, 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': False},
                'chat': {'id': 9887654321},
                'text': 'The quick brown fox jumps over the lazy dog'
                }

    def test_create_user(self, generate_data):
        data = generate_data
        user = app.create_user(data)
        assert user.id == data['from']['id']
        assert user.username == data['from']['username']
        assert user.first_name == data['from']['first_name']
        assert user.is_bot == data['from']['is_bot']
        assert user.chat_id == data['chat']['id']
        assert user.message == data['text']

    def test_create_user_with_bot(self, generate_data):
        data = generate_data
        data['from']['is_bot'] = True
        user = app.create_user(data)
        assert user.is_bot is True

    def test_create_user_with_no_text(self, generate_data):
        data = generate_data
        data['text'] = ''
        user = app.create_user(data)
        assert user.message == ''


class TestLoadAmountMl:
    def test_amount(self):
        text = '12.30pm 100ml'
        assert app.load_amount_ml(text) == 100

    def test_amount_not_found(self):
        text = '12.30pm'
        assert app.load_amount_ml(text) == -1

    def test_long_message(self):
        text = '12.30pm 80ml at home'
        assert app.load_amount_ml(text) == 80

    def test_multiple_amounts(self):
        text = '12.30pm 50ml 60ml at home'
        assert app.load_amount_ml(text) == 60


class TestReadAction:
    def test_record_milk(self):
        text = '12.30pm drink 100ml'
        assert app.read_message(text) == 'RECORD'

    def test_record_milk_space(self):
        text = '12.30pm drink 100ml '
        assert app.read_message(text) == 'RECORD'

    def test_record_milk_end(self):
        text = '12.30pm drink 100ml hot'
        assert app.read_message(text) == 'RECORD'

    def test_today(self):
        assert app.read_message('Today ') == 'TODAY'
        assert app.read_message('today ') == 'TODAY'
        assert app.read_message('today') == 'TODAY'

    def test_yesterday(self):
        assert app.read_message('Yesterday ') == 'YESTERDAY'
        assert app.read_message('yesterday ') == 'YESTERDAY'
        assert app.read_message('yesterday') == 'YESTERDAY'

    def test_unknown(self):
        assert app.read_message('hello world ') == 'UNKNOWN'

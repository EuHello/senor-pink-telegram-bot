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


class TestGetBotUrl:
    def test_get_bot_url(self):
        assert app.get_bot_url('TOKEN') == 'https://api.telegram.org/botTOKEN/sendMessage'


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
        amt = 100
        assert app.read_action('', amt) == 'RECORD'

    def test_no_milk_amount(self):
        amt = -1
        assert app.read_action('', amt) != 'RECORD'

    def test_today(self):
        assert app.read_action('Today ', -1) == 'TODAY'
        assert app.read_action('today ', -1) == 'TODAY'
        assert app.read_action('today', -1) == 'TODAY'

    def test_yesterday(self):
        assert app.read_action('Yesterday ', -1) == 'YESTERDAY'
        assert app.read_action('yesterday ', -1) == 'YESTERDAY'
        assert app.read_action('yesterday', -1) == 'YESTERDAY'

    def test_unknown(self):
        assert app.read_action('hello world ', -1) == 'UNKNOWN'

import pytest
import random

from . import context
from telegram_bot import app
from telegram_bot.user import TelegramUser


@pytest.fixture()
def test_allowed_users():
    return [12345678, 567890]


@pytest.fixture()
def generate_user():
    return TelegramUser(12345678, 'UserName123', 'Paul Atreides', False,
                        987654321, 'The quick brown fox jumps over the lazy dog')


@pytest.fixture
def generate_data():
    return {'from': {'id': 12345678, 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': False},
            'chat': {'id': 9887654321},
            'text': 'The quick brown fox jumps over the lazy dog'
            }


class TestCreateUser:
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
        assert user.is_bot == True


    def test_create_user_with_no_text(self, generate_data):
        data = generate_data
        data['text'] = ''
        user = app.create_user(data)
        assert user.message == ''


class TestValidateUser:
    def test_validate_1(self, generate_user, test_allowed_users):
        user = generate_user
        assert app.validate_user(user, test_allowed_users) == True

    def test_validate_2(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_id(567890)
        assert app.validate_user(user, test_allowed_users) == True

    def test_validate_user_not_in_list(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_id(9999)
        assert app.validate_user(user, test_allowed_users) == False

    def test_validate_bot(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_is_bot(True)
        assert app.validate_user(user, test_allowed_users) == False

    def test_validate_bot_none(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_is_bot(None)
        assert app.validate_user(user, test_allowed_users) == False

    def test_validate_bot_string(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_is_bot("False")
        assert app.validate_user(user, test_allowed_users) == False

    def test_validate_invalid_chat_id(self, generate_user, test_allowed_users):
        user = generate_user
        user.set_chat_id(-1)
        assert app.validate_user(user, test_allowed_users) == False


class TestGetBotUrl:
    def test_get_bot_url(self):
        assert app.get_bot_url('TOKEN') == 'https://api.telegram.org/botTOKEN/sendMessage'

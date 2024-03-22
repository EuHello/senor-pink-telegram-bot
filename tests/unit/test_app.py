import pytest
import random

from . import context
from telegram_bot import app
from telegram_bot.user import TelegramUser


@pytest.fixture()
def test_allowed_users():
    return [12345678, 567890]


@pytest.fixture
def user_valid_1():
    return TelegramUser(12345678, 'UserName12345', 'Paul Atreides', False,
                        9887654321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_valid_2():
    return TelegramUser(567890, 'UserName12345', 'Paul Atreides', False,
                        9887654321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_not_allowed():
    return TelegramUser(5555555, 'UserName12345', 'Jane', False,
                        9887654321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_bot():
    return TelegramUser(12345678, 'UserName12345', 'Jane', True,
                        321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_bot_none():
    return TelegramUser(12345678, 'UserName12345', 'Jane', None,
                        321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_bot_string():
    return TelegramUser(12345678, 'UserName12345', 'Jane', "False",
                        321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_invalid_chat_id():
    return TelegramUser(12345678, 'UserName12345', 'Jane', False,
                        -1, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_large_chat_id():
    return TelegramUser(12345678, 'UserName12345', 'James', False,
                        random.randint(12*10, 15*10), 'The quick brown fox jumps over the lazy dog')



@pytest.fixture
def data_valid():
    return {'from': {'id': 12345678, 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': False},
            'chat': {'id': 9887654321},
            'text': {'The quick brown fox jumps over the lazy dog'}
            }

@pytest.fixture
def data_bot():
    return {'from': {'id': 123, 'first_name': 'Jane', 'username': 'UserName12345', 'is_bot': True},
            'chat': {'id': 321},
            'text': {'The quick brown fox jumps over the lazy dog'}
            }

@pytest.fixture
def data_no_text():
    return {'from': {'id': 123, 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': True},
            'chat': {'id': random.randint(5*10, 11*10)},
            'text': {''}
            }

@pytest.fixture
def data_uid_large():
    return {'from': {'id': random.randint(11*10, 15*10), 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': False},
            'chat': {'id': 12345678},
            'text': {'The quick brown fox jumps over the lazy dog'}
            }

@pytest.fixture
def data_chat_id_large():
    return {'from': {'id': 12345678, 'first_name': 'Paul', 'username': 'UserName12345', 'is_bot': False},
            'chat': {'id': random.randint(12*10, 15*10)},
            'text': {'The quick brown fox jumps over the lazy dog'}
            }

class TestCreateUser:
    def test_create_user(self, data_valid):
        user = app.create_user(data_valid)
        assert user.id == data_valid['from']['id']
        assert user.username == data_valid['from']['username']
        assert user.first_name == data_valid['from']['first_name']
        assert user.is_bot == data_valid['from']['is_bot']
        assert user.chat_id == data_valid['chat']['id']
        assert user.message == data_valid['text']

    def test_create_user_with_bot(self, data_bot):
        user = app.create_user(data_bot)
        assert user.id == data_bot['from']['id']
        assert user.username == data_bot['from']['username']
        assert user.first_name == data_bot['from']['first_name']
        assert user.is_bot == data_bot['from']['is_bot']
        assert user.chat_id == data_bot['chat']['id']
        assert user.message == data_bot['text']


    def test_create_user_with_no_text(self, data_no_text):
        user = app.create_user(data_no_text)
        assert user.message == data_no_text['text']

    def test_create_user_with_largeuid(self, data_uid_large):
        user = app.create_user(data_uid_large)
        assert user.id == data_uid_large['from']['id']

    def test_create_user_with_largechatid(self, data_chat_id_large):
        user = app.create_user(data_chat_id_large)
        assert user.chat_id == data_chat_id_large['chat']['id']

class TestValidateUser:
    def test_validate_1(self, user_valid_1, test_allowed_users):
        assert app.validate_user(user_valid_1, test_allowed_users) == True

    def test_validate_2(self, user_valid_2, test_allowed_users):
        assert app.validate_user(user_valid_2, test_allowed_users) == True

    def test_validate_user_not_in_list(self, user_not_allowed, test_allowed_users):
        assert app.validate_user(user_not_allowed, test_allowed_users) == False

    def test_validate_bot(self, user_bot, test_allowed_users):
        assert app.validate_user(user_bot, test_allowed_users) == False

    def test_validate_bot_none(self, user_bot_none, test_allowed_users):
        assert app.validate_user(user_bot_none, test_allowed_users) == False

    def test_validate_bot_str(self, user_bot_string, test_allowed_users):
        assert app.validate_user(user_bot_string, test_allowed_users) == False

    def test_validate_invalid_chatid(self, user_invalid_chat_id, test_allowed_users):
        assert app.validate_user(user_invalid_chat_id, test_allowed_users) == False

    def test_validate_large_chatid(self, user_large_chat_id, test_allowed_users):
        assert app.validate_user(user_large_chat_id, test_allowed_users) == True

class TestGetBotUrl:
    def test_get_bot_url(self):
        assert app.get_bot_url('TOKEN') == 'https://api.telegram.org/botTOKEN/sendMessage'

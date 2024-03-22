import pytest

from . import context
from telegram_bot.user import TelegramUser


@pytest.fixture
def user_valid_1():
    return TelegramUser(12345678, 'UserName12345', 'Paul Atreides', False,
                        9887654321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_bot_none():
    return TelegramUser(12345678, 'UserName12345', 'Jane', None,
                        321, 'The quick brown fox jumps over the lazy dog')

@pytest.fixture
def user_bot_string():
    return TelegramUser(12345678, 'UserName12345', 'Jane', "False",
                        321, 'The quick brown fox jumps over the lazy dog')


class TestTelegramUser:
    def test_set_chat_id(self, user_valid_1):
        new_chat_id = 98765
        user = user_valid_1
        assert user.chat_id != new_chat_id
        user.set_chat_id(new_chat_id)
        assert user.chat_id == new_chat_id

    def test_set_message(self, user_valid_1):
        new_message = "Hello World"
        user = user_valid_1
        assert user.message != new_message
        user.set_message(new_message)
        assert user.message == new_message

    def test_validate_self(self, user_valid_1,):
        user = user_valid_1
        assert user.validate_self() == True

    def test_validate_bot_none(self, user_bot_none,):
        user = user_bot_none
        assert user.validate_self() == False

    def test_validate_bot_string(self, user_bot_string,):
        user = user_bot_string
        assert user.validate_self() == False

    def test_validate_message_object(self, user_valid_1,):
        user = user_valid_1
        assert user.validate_self() == True
        user.set_message({'hello': 'world'})
        assert user.validate_self() == False

import pytest

from . import context
from telegram_bot.user import TelegramUser


@pytest.fixture
def generate_user():
    return TelegramUser(12345678, 'UserName123', 'Paul Atreides', False,
                        987654321, 'The quick brown fox jumps over the lazy dog')


class TestSetId:
    def test_set_id(self, generate_user):
        new_id = 321
        user = generate_user
        assert user.id != new_id
        user.set_id(new_id)
        assert user.id == new_id


class TestSetIsBot:
    def test_set_is_bot(self, generate_user):
        new_is_bot = True
        user = generate_user
        assert user.is_bot != new_is_bot
        user.set_is_bot(new_is_bot)
        assert user.is_bot == new_is_bot


class TestSetChatId:
    def test_set_chat_id(self, generate_user):
        new_chat_id = 98765
        user = generate_user
        assert user.chat_id != new_chat_id
        user.set_chat_id(new_chat_id)
        assert user.chat_id == new_chat_id


class TestSetMessage:
    def test_set_message(self, generate_user):
        new_message = "Hello World"
        user = generate_user
        assert user.message != new_message
        user.set_message(new_message)
        assert user.message == new_message


class TestValidateSelf:
    def test_validate_self(self, generate_user):
        user = generate_user
        assert user.validate_self() is True

    def test_bot_none(self, generate_user):
        user = generate_user
        assert user.validate_self() is True
        user.set_is_bot(None)
        assert user.validate_self() is False

    def test_bot_string(self, generate_user):
        user = generate_user
        assert user.validate_self() is True
        user.set_is_bot("False")
        assert user.validate_self() is False

    def test_message_object(self, generate_user):
        user = generate_user
        assert user.validate_self() is True
        user.set_message({'hello': 'world'})
        assert user.validate_self() is False

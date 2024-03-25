import pytest

from . import context
from telegram_bot.reply import Reply


class TestReply:
    @pytest.fixture
    def generate_reply(self):
        return Reply('Hello_World')

    def test_escape_variable_name(self, generate_reply):
        reply = generate_reply
        assert reply.escape_variable_name() == 'Hello%5FWorld'

    def test_join_secret_ext_endpoint(self, generate_reply):
        reply = generate_reply
        assert (reply.join_secret_ext_endpoint('FOO') ==
                'http://localhost:2773/systemsmanager/parameters/get?name=FOO&withDecryption=true')

    def test_join_telegram_endpoint(self, generate_reply):
        reply = generate_reply
        assert reply.join_telegram_endpoint('TOKEN') == 'https://api.telegram.org/botTOKEN/sendMessage'

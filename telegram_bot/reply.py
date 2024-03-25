import os
import requests
import logging


logger = logging.getLogger(__name__)


class Reply:
    """Sends a text message to the Telegram user"""
    # Telegram API
    api_base_url = 'https://api.telegram.org/bot'
    api_method = 'sendMessage'

    # AWS SSM / Parameter Store secrets
    secret_ext_port = '2773'

    def __init__(self, token_name):
        self.secret_variable_name = token_name

    def escape_variable_name(self):
        """Escapes variable name for url"""
        return self.secret_variable_name.replace('_', '%5F')

    def join_secret_ext_endpoint(self, secret_name_path):
        """creates url for AWS store API"""
        return (f'http://localhost:{self.secret_ext_port}/systemsmanager/parameters/'
                f'get?name={secret_name_path}&withDecryption=true')

    def load_bot_token(self):
        """Get telegram bot token from AWS Parameter Store via API with 'AWS Parameters and Secrets Lambda Extension'.

        Returns:
        secret: str, secret token from AWS Parameter Store
        """
        secret_name_path = self.escape_variable_name()
        secret_ext_endpoint = self.join_secret_ext_endpoint(secret_name_path)

        headers = {'X-Aws-Parameters-Secrets-Token': os.environ.get('AWS_SESSION_TOKEN')}
        r = requests.get(secret_ext_endpoint, headers=headers)

        if r.status_code != 200:
            logger.exception(f'Unable to retrieve token from AWS store. r.status_code={r.status_code}')
            raise

        # secret_name = json.loads(response)['Parameter']['Name']
        secret = r.json()['Parameter']['Value']

        return secret

    def join_telegram_endpoint(self, token):
        """Return telegram API url from telegram token. Format: https://api.telegram.org/bot<token>/METHOD_NAME"""
        url = f'{self.api_base_url}{token}/{self.api_method}'
        return url

    def send_text(self, chat_id: int, reply_message: str):
        """Sends message to user via Telegram API. Returns response.json()

        Params:
        chat_id:         int, chat_id of user
        reply_message:   str, text message to the user
        """
        token = self.load_bot_token()
        if not isinstance(token, str):
            logger.exception(f'Token is not string type. token={token}, type token={type(token)}')
            raise

        reply_endpoint = self.join_telegram_endpoint(token)

        params = {'chat_id': chat_id, 'text': reply_message}
        response = requests.post(reply_endpoint, json=params)

        return response.json()

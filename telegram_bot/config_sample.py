# Configuration for Lambda Handler app.py

# Environment
ENV = 'DEV'    # 'PROD'


# BOT API to send message
BOT_BASE_URL = 'https://api.telegram.org/bot'
BOT_METHOD = 'sendMessage'
BOT_TOKEN_NAME = 'your bot token (environment variable) name'
# https://api.telegram.org/bot<token>/METHOD_NAME


# Define PATHS for AWS SSM / Parameter Store secrets
TOKEN_PARAM_PATH = 'YourTokenNamePath'
SECRET_EXT_PORT = '2773'


# Configuration of Allowed Users
allowed_ids = [123, 321]

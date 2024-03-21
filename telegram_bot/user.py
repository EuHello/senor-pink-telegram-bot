class TelegramUser:
    def __init__(self, user_id: int, username: str, first_name: str, is_bot: bool):
        self.uid = user_id
        self.name = username
        self.first_name = first_name
        self.is_bot = is_bot
        self.chat_id = -1
        self.message = ''

    def add_chat_id(self, chat_id: int):
        self.chat_id = chat_id

    def add_first_name(self, first_name: str):
        if first_name is not None:
            self.first_name = first_name

    def add_username(self, username: str):
        if username is not None:
            self.name = username

    def add_is_bot(self, is_bot: bool):
        if isinstance(is_bot, bool):
            self.is_bot = is_bot

    def add_message(self, message: str):
        if message is not None and len(message) > 0:
            self.message = message

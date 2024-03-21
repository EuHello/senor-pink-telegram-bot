class TelegramUser:
    def __init__(self, user_id: int, username: str, first_name: str, is_bot: bool):
        self.uid = user_id
        self.name = username
        self.first_name = first_name
        self.is_bot = is_bot
        self.chat_id = -1
        self.message = ''

    def set_chat_id(self, chat_id: int):
        self.chat_id = chat_id

    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def set_username(self, username: str):
        self.name = username

    def set_is_bot(self, is_bot: bool):
        self.is_bot = is_bot

    def set_message(self, message: str):
        self.message = message

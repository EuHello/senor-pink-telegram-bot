import config as cfg


class TelegramUser:
    def __init__(self, id: int, first_name: str, is_bot: bool, chat_id: int, message: str):
        self.id = id
        self.first_name = first_name
        self.is_bot = is_bot
        self.chat_id = chat_id
        self.message = message

    def set_id(self, id: int):
        self.id = id

    def set_is_bot(self, is_bot: bool):
        self.is_bot = is_bot

    def set_chat_id(self, chat_id: int):
        self.chat_id = chat_id

    def set_message(self, message: str):
        self.message = message

    def validate_self(self, allowed_users=cfg.allowed_ids):
        """Validates TelegramUser instance.

        Params:
        allowed_users: list, allowed user ids from config. Default = list from config

        Returns:
        True:  bool, user is validated and found within the allowed list
        False: bool, user is not validated
        """
        return (
                isinstance(self.id, int) and
                isinstance(self.first_name, str) and isinstance(self.is_bot, bool) and
                isinstance(self.chat_id, int) and isinstance(self.message, str) and
                not self.is_bot and (self.id in allowed_users)
        )

import requests

__all__ = ["Message"]

with open("token.txt", 'r') as file:
    TOKEN = file.read()

TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


class Message:
    def __init__(self, message):
        self.message: dict = message
        self.real_message: dict = message['message']
        self._chat_id = self.real_message['chat']['id']

    def text(self):
        return self.real_message.get('text', None)

    def chat_id(self):
        return self._chat_id

    def full_name(self):
        return f"{self.real_message['from']['first_name']} {self.real_message['from']['last_name']}"

    def username(self):
        return self.real_message['from']['username']

    def sticker(self):
        sticker = self.real_message.get('sticker', None)
        if 'sticker' is None:
            return None
        return sticker['set_name']

    def send_message(self, **kwargs):
        payload = {
            'chat_id': self._chat_id,
            'parse_mode': "HTML",
            **kwargs
        }
        r = requests.post(TELEGRAM_URL, json=payload)
        return r

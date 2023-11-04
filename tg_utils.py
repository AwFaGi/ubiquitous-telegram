import requests

__all__ = ["Message", "StickerSet"]

with open("token.txt", 'r') as file:
    TOKEN = file.read()

TELEGRAM_SEND_MESSAGE = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
TELEGRAM_SEND_STICKER = f'https://api.telegram.org/bot{TOKEN}/sendSticker'
TELEGRAM_STICKER = f'https://api.telegram.org/bot{TOKEN}/getStickerSet'


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
        r = requests.post(TELEGRAM_SEND_MESSAGE, json=payload)
        return r

    def send_sticker(self, **kwargs):
        payload = {
            'chat_id': self._chat_id,
            **kwargs
        }
        r = requests.post(TELEGRAM_SEND_STICKER, json=payload)
        return r


class StickerSet:
    def __init__(self, name):

        payload = {
            'name': name
        }

        r = requests.get(TELEGRAM_STICKER, params=payload)
        sticker_set = r.json()
        print(sticker_set)
        self.sticker_set: dict = sticker_set['result']

    def get_sticker_list(self):
        return self.sticker_set['stickers']
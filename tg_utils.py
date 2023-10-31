import requests

__all__ = ["parse_message", "send_message"]

with open("/home/AwFaGi/bot/token.txt", 'r') as file:
    TOKEN = file.read()


def parse_message(message):
    real_message = message['message']
    chat_id = real_message['chat']['id']
    txt = real_message['text'] if 'text' in real_message else None
    name = f"{real_message['from']['first_name']} {real_message['from']['last_name']}"
    return chat_id, txt, name


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': "HTML"
    }

    r = requests.post(url, json=payload)
    return r

import random

from cock_controller import CockController
from tg_utils import Message

__all__ = ["process_command", "process_random_choice", "process_content"]
cock_controller = CockController()


def start_func(message: Message):
    result = {
        'text': "Привет! Я помогу тебе сделать выбор в трудной ситуации. Попробуй написать /help"
    }
    message.send_message(**result)


def help_func(message: Message):
    s = "Для выбора текстовых значений, напиши их по одному в строке.\n" \
        "<i>Фотографии пока недоступны</i>\n" + \
        "\n".join([f"{i}: {bot_commands[i][1]}" for i in bot_commands.keys()])

    result = {
        'text': s
    }
    message.send_message(**result)


def range_func(message: Message):
    args = message.text().split()[1:]
    try:
        arguments = list(map(int, args))
        if len(arguments) == 0:
            result = {
                'text': str(random.randrange(1, 101))
            }
        else:
            result = {
                'text': str(random.randrange(*arguments))
            }
        message.send_message(**result)
    except Exception:
        s = (
            "<b>Произошла ошибка!</b>\n"
            "Правильное использование:\n"
            "/range конец\n"
            "/range начало конец\n"
            "/range начало конец шаг\n"
        )
        result = {
            'text': s
        }
        message.send_message(**result)


def cock_func(message: Message):
    name = message.full_name()
    chat_id = message.chat_id()

    cock_size = cock_controller.get(chat_id)
    result_string = f"{name}, your cock is {cock_size} cm"

    result = {
        'text': result_string
    }

    message.send_message(**result)


bot_commands = {
    "/start": (start_func, "Приветствует пользователя"),
    "/help": (help_func, "Пишет данную справку."),
    "/range": (range_func,
               "Принимает до 3 целых чисел. "
               "Возвращает целое число из указанного промежутка. "
               "По умолчанию: диапазон 1-100"
               ),
    "/cock_size": (cock_func, "Измеряет так называемый cock")
}


def process_command(message: Message):
    text = message.text()

    maybe_command = text.split()[0]
    if maybe_command in bot_commands:
        command = bot_commands[maybe_command][0]
        command(message)
        return True
    else:
        return False


def process_random_choice(message: Message):
    text = message.text()

    variants = text.splitlines()
    cash = dict([(i, 0) for i in variants])
    for i in range(100):
        cash[random.choice(variants)] += 1
    m = max(cash, key=lambda i: cash[i])
    mes = (
        f"<i>{m}</i>\n\n"
        "<span class='tg-spoiler'>"
        f"Было выбрано после 100 итераций, с процентом побед <b>{cash[m]}%</b>"
        "</span>"
    )

    result = {
        'text': mes
    }

    message.send_message(**result)


def process_content(message: Message):

    if message.sticker() is not None:
        text = f"Красивый стикер.\nЯ знаю, что он из пака: <code>{message.sticker()}</code>"
    else:
        text = "Я не смог обработать Ваше сообщение"

    result = {
        'text': text
    }

    message.send_message(**result)

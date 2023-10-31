import random

from cock_controller import CockController
from tg_utils import send_message


__all__ = ["process_command", "process_random_choice"]
cock_controller = CockController()


def start_func(chat_id, *args, **kwargs):
    send_message(
        chat_id,
        "Привет! Я помогу тебе сделать выбор в трудной ситуации. Попробуй написать /help"
    )


def help_func(chat_id, *args, **kwargs):
    s = "Для выбора текстовых значений, напиши их по одному в строке.\n" \
        "<i>Фотографии пока недоступны</i>\n" + \
        "\n".join([f"{i}: {bot_commands[i][1]}" for i in bot_commands.keys()])

    send_message(
        chat_id,
        s
    )


def range_func(chat_id, *args, **kwargs):
    try:
        arguments = list(map(int, args))
        if len(arguments) == 0:
            send_message(
                chat_id,
                str(random.randrange(1, 101))
            )
        else:
            send_message(
                chat_id,
                str(random.randrange(*arguments))
            )
    except Exception:
        s = (
            "<b>Произошла ошибка!</b>\n"
            "Правильное использование:\n"
            "/range конец\n"
            "/range начало конец\n"
            "/range начало конец шаг\n"
        )
        send_message(
            chat_id,
            s
        )


def cock_func(chat_id, *args, **kwargs):
    name = kwargs['name']
    cock_size = cock_controller.get(chat_id)

    result_string = f"{name}, your cock is {cock_size} cm"

    send_message(
        chat_id,
        result_string
    )


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


def process_command(chat_id, text, name):
    maybe_command = text.split()[0]
    if maybe_command in bot_commands:
        command = bot_commands[maybe_command][0]
        command(chat_id, *text.split()[1:], name=name)
        return True
    else:
        return False


def process_random_choice(chat_id, text):
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

    send_message(
        chat_id,
        mes
    )

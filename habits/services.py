import os

import requests


# Функция рассылки сообщений в телеграмм пользователям
def send_message(habit):
    TELEGRAMM_KEY = os.getenv('TELEGRAMM_KEY')
    if habit.related_habit:
        data = {
            "chat_id": habit.owner.chat_id,
            "text": f"Пора выполнить {habit.action} в {habit.place}."
                    f"Не забудьте также выполнить {habit.related_habit.action} в {habit.related_habit.place}"
        }
    elif habit.reward:
        data = {
            "chat_id": habit.owner.chat_id,
            "text": f"Пора выполнить {habit.action} в {habit.place}."
                    f"За выполнение вам предоставляется награда {habit.reward}"
        }
    else:
        data = {
            "chat_id": habit.owner.chat_id,
            "text": f"Пора выполнить {habit.action} в {habit.place}."
        }
    if habit.owner.chat_id:
        try:
            requests.post(f"https://api.telegram.org/bot{TELEGRAMM_KEY}/sendMessage", data=data)
        except Exception:
            raise Exception("Ошибка отправки сообщения пользователю {habit.owner.email}")
    else:
        raise Exception(f"У пользователя {habit.owner.email} не указан chat_id для рассылки сообщений")

from datetime import datetime, timedelta

from celery import shared_task

from habits.models import Habit
from habits.services import send_message


# Функция для выполнени периодической задачи по рассылке сообщений
@shared_task
def sending_reminders():
    for habit in Habit.objects.filter(is_pleasant=False):
        if habit.time.replace(tzinfo=None) == datetime.now().replace(second=0, microsecond=0):
            send_message(habit)
            if habit.period == 'каждый час':
                habit.time += timedelta(hours=1)
            elif habit.period == 'каждый день':
                habit.time += timedelta(days=1)
            elif habit.period == 'каждую неделю':
                habit.time += timedelta(days=7)
            habit.save()

from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    PERIOD = (
        ('каждый час', 'каждый час'),
        ('каждый день', 'каждый день'),
        ('каждую неделю', 'каждую неделю'),
        ('каждый месяц', 'каждый месяц')
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='создатель')
    place = models.CharField(max_length=200, **NULLABLE, verbose_name='место выполнения')
    time = models.DateTimeField(**NULLABLE, verbose_name='дата и время выполнения')
    action = models.CharField(max_length=500, **NULLABLE, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, verbose_name='связанная привычка')
    period = models.CharField(default='каждый день', max_length=30, verbose_name='периодичность выполнения привычки',
                              choices=PERIOD)
    reward = models.TextField(verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveIntegerField(default=60, **NULLABLE, verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

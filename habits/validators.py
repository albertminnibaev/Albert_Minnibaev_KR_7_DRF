import datetime
from rest_framework.serializers import ValidationError


class TimeToCompleteValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд')


class PeriodValidator:
    PERIOD = (
        'каждый час',
        'каждый день',
        'каждую неделю',
    )

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value not in self.PERIOD:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

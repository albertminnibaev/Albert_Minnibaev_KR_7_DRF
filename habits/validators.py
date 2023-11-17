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


class RelatedHabitOrRewardValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = dict(value).get(self.field[0])
        reward = dict(value).get(self.field[1])
        if related_habit and reward:
            raise ValidationError('Нельзя одновременно производить выбор связанной привычки и указания вознаграждения')


class RelatedHabitValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = dict(value).get(self.field[0])
        # current_user = dict(value).get(self.field[1])
        print(related_habit)
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной привычки')
        # if related_habit and related_habit.owner != current_user:
        #     print(related_habit.owner)
        #     print(current_user)
        #     raise ValidationError(
        #         'В связанные привычки могут попадать только привычки, созанные вами')


class IsPleasantValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasant = dict(value).get(self.field[0])
        related_habit = dict(value).get(self.field[1])
        reward = dict(value).get(self.field[2])
        if is_pleasant and (related_habit or reward):
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки')

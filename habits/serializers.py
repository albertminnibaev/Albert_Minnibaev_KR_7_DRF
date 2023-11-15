from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeToCompleteValidator, PeriodValidator


class HabitCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeToCompleteValidator(field='time_to_complete'),
            PeriodValidator(field='period')
        ]


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'

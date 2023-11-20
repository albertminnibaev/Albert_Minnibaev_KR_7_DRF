from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeToCompleteValidator, PeriodValidator, RelatedHabitOrRewardValidator, \
    RelatedHabitValidator, IsPleasantValidator


class HabitCreateSerializer(serializers.ModelSerializer):

    def validate_related_habit(self, value):
        user = self.context['request'].user
        if value.owner == user:
            return value
        raise serializers.ValidationError('В связанные привычки могут попадать только привычки, созданные вами')

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeToCompleteValidator(field='time_to_complete'),
            PeriodValidator(field='period'),
            RelatedHabitOrRewardValidator(field=('related_habit', 'reward')),
            RelatedHabitValidator(field='related_habit'),
            IsPleasantValidator(field=('is_pleasant', 'related_habit', 'reward'))
        ]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

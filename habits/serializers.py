from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeToCompleteValidator, PeriodValidator, RelatedHabitOrRewardValidator, \
    RelatedHabitValidator, IsPleasantValidator


class HabitCreateSerializer(serializers.ModelSerializer):

    # current_user = serializers.SerializerMethodField('_user')
    #
    # def _user(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return request.user
    #
    # def _user(self, obj):
    #     return self.context['request'].user

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            TimeToCompleteValidator(field='time_to_complete'),
            PeriodValidator(field='period'),
            RelatedHabitOrRewardValidator(field=('related_habit', 'reward')),
            RelatedHabitValidator(field=('related_habit', 'current_user')),
            IsPleasantValidator(field=('is_pleasant', 'related_habit', 'reward'))
        ]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

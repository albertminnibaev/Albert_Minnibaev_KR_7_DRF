from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'time', 'action', 'is_pleasant', 'related_habit', 'period', 'reward',
                    'time_to_complete', 'is_public')

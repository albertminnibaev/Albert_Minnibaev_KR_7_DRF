from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitCreateSerializer, HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['user'] = self.queryset.user
    #     return context


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    # Переопределение метода get_queryset, для вывода списка привычек принадлежащих только данному пользователю
    def get_queryset(self):
        object = super().get_queryset().filter(owner=self.request.user)
        return object


class HabitListPublicAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    # Переопределение метода get_queryset, для вывода списка привычек со статусом публичные
    def get_queryset(self):
        object = super().get_queryset().filter(is_public=True)
        return object


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitCreateSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

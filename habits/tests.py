from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            place="кухня",
            time="2023-11-17 18:00:00+00:00",
            action="съесть конфету",
            is_pleasant="False",
            period="каждый день",
            time_to_complete="100",
            is_public="True",
            reward='конфета'
            # related_habit="4"
        )

    def test_create_habit(self):
        """ Тестирование создания привычки """

        data = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': (self.habit.id + 1),
             'place': self.habit.place,
             'time': '2023-11-17T18:00:00Z',
             'action': self.habit.action,
             'is_pleasant': False,
             'period': self.habit.period,
             'time_to_complete': 100,
             'is_public': True,
             'reward': self.habit.reward,
             'owner': self.user.id,
             'related_habit': None}
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_list_habit(self):
        """ Тестирование просмотра списка привычек пользователя """

        # создаем новую привычку авторизированным пользователем
        data_1 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data_1
        )

        response = self.client.get(
            '/habits/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{'id': (self.habit.id + 1),
              'place': self.habit.place,
              'time': '2023-11-17T18:00:00Z',
              'action': self.habit.action,
              'is_pleasant': False,
              'period': self.habit.period,
              'time_to_complete': 100,
              'is_public': True,
              'reward': self.habit.reward,
              'owner': self.user.id,
              'related_habit': None}]
        )

    def test_list_public_habit(self):
        """ Тестирование просмотра списка публичных привычек """

        response = self.client.get(
            '/habits/public/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{'id': self.habit.id,
              'place': self.habit.place,
              'time': '2023-11-17T18:00:00Z',
              'action': self.habit.action,
              'is_pleasant': False,
              'period': self.habit.period,
              'time_to_complete': 100,
              'is_public': True,
              'reward': self.habit.reward,
              'owner': None,
              'related_habit': None}]
        )

    def test_retrieve_habit(self):
        """ Тестирование просмотра одной привычки """

        # создаем новую привычку авторизированным пользователем
        data_1 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data_1
        )

        # запрос на просмотр привычки
        response = self.client.get(
            f'/habits/{(self.habit.id + 1)}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': (self.habit.id + 1),
             'place': self.habit.place,
             'time': '2023-11-17T18:00:00Z',
             'action': self.habit.action,
             'is_pleasant': False,
             'period': self.habit.period,
             'time_to_complete': 100,
             'is_public': True,
             'reward': self.habit.reward,
             'owner': self.user.id,
             'related_habit': None}
        )

    def test_update_habits(self):
        """ Тестирование обновления привычки """

        # создаем новую привычку авторизированным пользователем
        data_1 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data_1
        )

        # запрос на обновление привычки
        data = {
            'place': 'место'
        }
        response = self.client.patch(
            f'/habits/update/{self.habit.id + 1}/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': (self.habit.id + 1),
             'place': 'место',
             'time': '2023-11-17T18:00:00Z',
             'action': self.habit.action,
             'is_pleasant': False,
             'period': self.habit.period,
             'time_to_complete': 100,
             'is_public': True,
             'reward': self.habit.reward,
             'owner': self.user.id,
             'related_habit': None}
        )

    def test_destroy_habits(self):
        """ Тестирование удаления привычки """

        # создаем новую привычку авторизированным пользователем
        data_1 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data_1
        )

        response = self.client.delete(
            f'/habits/delete/{self.habit.id + 1}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

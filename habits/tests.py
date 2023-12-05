import os

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from habits.services import send_message
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test', is_staff=True,
                                        is_superuser=True, chat_id=os.getenv('CHAT_ID'))
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

    def test_str_verbose_habits(self):
        habit = Habit.objects.create(
            place="кухня",
            time="2023-11-17 18:00:00+00:00",
            action="съесть конфету",
            is_pleasant="False",
            period="каждый день",
            time_to_complete="100",
            is_public="True",
            reward='конфета'
        )

        self.assertEqual(
            habit.__str__(),
            "съесть конфету в 2023-11-17 18:00:00+00:00 в кухня"
        )

        self.assertEqual(
            habit._meta.verbose_name,
            "привычка"
        )

    def test_str_verbose_user(self):
        self.assertEqual(
            self.user.__str__(),
            f'{self.user.email}, {self.user.phone}, {self.user.city}'
        )

        self.assertEqual(
            self.user._meta.verbose_name,
            "user"
        )

        self.assertEqual(
            self.user._meta.verbose_name_plural,
            "users"
        )

    def test_send_message(self):
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

        send_message(Habit.objects.filter(id=(self.habit.id + 1))[0])

    def test_send_message_2(self):

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

        self.user.chat_id = ''
        self.user.save()

        with self.assertRaises(Exception):
            send_message(Habit.objects.filter(id=(self.habit.id + 1))[0])

    def test_send_message_3(self):

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

        self.user.chat_id = '123455555555556'
        self.user.save()

        # self.assertFalse(
        #     send_message(Habit.objects.filter(id=(self.habit.id + 1))[0])
        # )
        #some_cool_exception = Exception("У пользователя test@test.com не указан chat_id для рассылки сообщений")

        self.assertRaises(
            Exception,
            send_message(Habit.objects.filter(id=(self.habit.id + 1))[0]),
        )

        # with self.assertRaises(Exception):
        #     send_message(Habit.objects.filter(id=(self.habit.id + 1))[0])

    def test_update_user(self):
        """ Тестирование обновления пользователя """

        # запрос на обновление пользователя
        data = {
            "first_name": "Admin",
        }
        response = self.client.patch(
            f'/users/update/{self.user.id}/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_user(self):
        """ Тестирование просмотра списка пользователей """

        # запрос на просмотр списка пользователей

        response = self.client.get(
            f'/users/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_related_habit(self):
        """ Тестирование обновления привычки """

        # создаем новую привычку авторизированным пользователем
        data_1 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': True,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
            # 'reward': self.habit.reward
        }

        response = self.client.post(
            '/habits/create/',
            data=data_1
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # создаем новую привычку авторизированным пользователем
        data_2 = {
            'place': self.habit.place,
            'time': self.habit.time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'period': self.habit.period,
            'time_to_complete': self.habit.time_to_complete,
            'is_public': self.habit.is_public,
        }

        response = self.client.post(
            '/habits/create/',
            data=data_2
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # запрос на обновление привычки
        data = {
            'related_habit': (self.habit.id + 1)
        }
        response = self.client.patch(
            f'/habits/update/{self.habit.id + 2}/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': (self.habit.id + 2),
             'place': self.habit.place,
             'time': '2023-11-17T18:00:00Z',
             'action': self.habit.action,
             'is_pleasant': False,
             'period': self.habit.period,
             'time_to_complete': 100,
             'is_public': True,
             'reward': None,
             'owner': self.user.id,
             'related_habit': self.habit.id + 1}
        )

    # def test_retrieve_user(self):
    #     """ Тестирование просмотра данных пользователя """
    #
    #     # запрос на просмотр
    #
    #     response = self.client.get(
    #         f'/users/{self.user.id}/',
    #
    #     )
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #
    #     # self.assertEqual(
    #     #     response.json(),
    #     #     [{'id': 5, 'password': 'test', 'last_login': None, 'is_superuser': True, 'first_name': '', 'last_name': '',
    #     #       'is_staff': True, 'is_active': True, 'date_joined': '2023-11-20T16:58:36.814554Z',
    #     #       'email': 'test@test.com', 'phone': None, 'avatar': None, 'city': None, 'chat_id': None,
    #     #       'groups': [], 'user_permissions': []}]
    #     # )
    #
    #     self.assertTrue(
    #         User.objects.all().exists()
    #     )
    #

    def test_register_user(self):
        """ Тестирование регистрации пользователя """

        data = {
            "email": "4@yandex.ru",
            "password": "123qwe456rty",
            "first_name": "Admin",
            "last_name": "Adminov",
            "is_superuser": "False",
            "is_staff": "False",
            "is_active": "True",
            'groups': [],
            'user_permissions': []
        }

        # запрос на регистрацию
        response = APIClient().post(
            f'/users/register/',
            data=data
        )
        print(response)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.all().exists()
        )

    # self.assertEqual(
    #     response.json(),
    #     {'id': (self.habit.id + 1),
    #      'place': 'место',
    #      'time': '2023-11-17T18:00:00Z',
    #      'action': self.habit.action,
    #      'is_pleasant': False,
    #      'period': self.habit.period,
    #      'time_to_complete': 100,
    #      'is_public': True,
    #      'reward': self.habit.reward,
    #      'owner': self.user.id,
    #      'related_habit': None}
    # )

    # class HabitTestCase_1(APITestCase):
    #
    #     def setUp(self) -> None:
    #         self.client = APIClient()
    #         self.user = User.objects.create(email='test@test.com', password='test', is_staff=True, is_superuser=True)
    #         self.client.force_authenticate(user=self.user)
    #
    #         self.habit = Habit.objects.create(
    #             place="кухня",
    #             time="2023-11-17 18:00:00+00:00",
    #             action="съесть конфету",
    #             is_pleasant="False",
    #             period="каждый день",
    #             time_to_complete="100",
    #             is_public="True",
    #             reward='конфета'
    #             # related_habit="4"
    #         )
    #
    #     def test_create_habit_1(self):
    #         """ Тестирование создания привычки """
    #
    #         data = {
    #             'place': 'улица',
    #             'time': '2023-11-17 18:00:00+00:00',
    #             'action': 'бег',
    #             'is_pleasant': False,
    #             #'related_habit': self.habit.id,
    #             'period': 'каждый час',
    #             'time_to_complete': 1300,
    #             'is_public': True,
    #             'reward': 'вода'
    #         }
    #
    #         response = self.client.post(
    #             '/habits/create/',
    #             data=data
    #         )
    #     #
    #     #     with self.assertRaises(ValidationError) as cm:
    #     #         self.habit.full_clean()
    #     #
    #     #     self.assertTrue('Время выполнения должно быть не больше 120 секунд' in cm.exception.message_dict)
    #
    #         self.assertEqual(
    #             response.status_code,
    #             status.HTTP_400_BAD_REQUEST
    #         )
    #         print(response.json())
    #
    # self.assertContains(
    #     response,
    #     'Время выполнения должно быть не больше 120 секунд'
    # )
    #
    #
    # self.assertEqual(
    #     response.json(),
    #     {'id': (self.habit.id + 1),
    #      'place': 'улица',
    #      'time': '2023-11-17T18:00:00Z',
    #      'action': 'бег',
    #      'is_pleasant': False,
    #      'period': 'каждый час',
    #      'time_to_complete': 80,
    #      'is_public': True,
    #      'reward': 'вода',
    #      'owner': self.user.id,
    #      'related_habit': None}
    # )
    #
    # self.assertTrue(
    #     Habit.objects.all().exists()
    # )

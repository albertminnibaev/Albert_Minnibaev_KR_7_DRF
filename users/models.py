from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'null': True, 'blank': True}


# class UserRole(models.TextChoices):
#     MODERATOR = 'moderator', _('moderator')
#     MEMBER = 'member', _('member')


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    chat_id = models.CharField(max_length=50, verbose_name='chat_id телеграмм', **NULLABLE)
    # role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}, {self.phone}, {self.city}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

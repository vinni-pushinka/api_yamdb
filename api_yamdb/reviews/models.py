from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        blank=False,
        max_length=150,
        unique=True,
        validators=[RegexValidator(
                '^[\w.@+-]+\z',
                message='Имя пользователя может содержать буквы, цифры и символы: @/./+/-/'
            )]
    )
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        blank=True,
        max_length=150
    )
    last_name = models.CharField(
        blank=True,
        max_length=150
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        choices=ROLES,
        default=USER,
    )

import datetime

from rest_framework.exceptions import ValidationError
from reviews.models import User


def validate_username(value):
    """Валидатор имени пользователя."""
    if value == "me":
        raise ValidationError("Недопустимое имя пользователя!")
    elif User.objects.filter(username=value).exists():
        raise ValidationError(
            "Пользователь с таким именем уже зарегистрирован"
        )


def validate_email(value):
    """Валидатор почты пользователя."""
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            "Пользователь с такой почтой уже зарегистрирован"
        )


def validate_title_year(value):
    year = datetime.date.today().year
    if value > year:
        raise ValidationError(
            'Год не может быть больше текущего!'
        )
    return value

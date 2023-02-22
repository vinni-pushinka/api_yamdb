from rest_framework.exceptions import ValidationError
from reviews.models import User


def validate_username(value):
    """Валидатор имени пользователя"""
    if value == "me":
        raise ValidationError("Недопустимое имя пользователя!")
    elif User.objects.filter(username=value).exists():
        raise ValidationError(
            "Пользователь с таким именем " "уже зарегестрирован"
        )


def validate_email(value):
    """Валидатор почты пользователя"""
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            "Пользователь с такой почтой " "уже зарегестрирован"
        )

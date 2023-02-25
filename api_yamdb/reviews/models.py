from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    class UserRole(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    role = models.CharField(
        max_length=255,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name="Роль"
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Логин",
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Допустимые символы: буквы, цифры и @/./+/-/_",
            )
        ],
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Почта"
    )
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name="Имя"
    )
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name="Фамилия"
    )
    bio = models.TextField(blank=True, verbose_name="Биография")

    confirmation_code = models.CharField(
        verbose_name="Токен пользователя",
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        max_length=256,
        default="Отсутствует",
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Slug категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Slug жанра"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=256, verbose_name="Название произведения"
    )
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска",)
    description = models.TextField(null=True, verbose_name="Описание")

    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        related_name="titles",
        verbose_name="Slug жанра",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Slug категории",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи жанр-произведение."""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
        help_text="Произведение, к которому будет написан отзыв",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text="Введите текст отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = [
            "-pub_date",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review",
            ),
        ]

    def __str__(self):
        return f"{self.title}, {self.score}, {self.author}"


class Comment(models.Model):
    """Модель комментария к отзыву."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="username автора комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарий",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    pub_date = models.DateTimeField(
        "Дата публикации комментария",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["pub_date"]

    def __str__(self):
        return self.text

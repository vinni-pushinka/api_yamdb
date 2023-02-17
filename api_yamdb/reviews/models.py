from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLES = (
    (USER, "user"),
    (MODERATOR, "moderator"),
    (ADMIN, "admin"),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, verbose_name="Логин"
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
    role = models.CharField(
        max_length=255, choices=ROLES, default=USER, verbose_name="Роль"
    )

    class Meta:
        verbose_name = "Пользователь"

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
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

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название жанра")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Slug жанра"
    )

    class Meta:
        verbose_name = "Жанр"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name="Название произведения"
    )
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание")

    genre = models.ManyToManyField(
        Genre, blank=True, related_name="titles", verbose_name="Slug жанра"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
        verbose_name="Slug категории",
    )

    class Meta:
        verbose_name = "Произведение"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель Отзыва на Title (Произведение)."""

    title = models.ForeignKey(
        Title,
        # Удаление Отзыва при удалении Произведения
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
        help_text="Произведение, к которому будет написан отзыв",
    )
    author = models.ForeignKey(
        User,
        # Удаление Отзыва при удалении Автора
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text="Введите текст отзыва",
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["pub_date"]


class Comment(models.Model):
    """Модель Комментария к Review (Отзыв)."""

    author = models.ForeignKey(
        User,
        # Удаление Комментария при удалении Автора
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="username автора комментария",
    )
    review = models.ForeignKey(
        Review,
        # Удаление Комментария при удалении Отзыва
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
        ordering = ["pub_date"]

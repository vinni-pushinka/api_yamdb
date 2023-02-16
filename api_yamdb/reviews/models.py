from django.db import models
from .validators import validate_score


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
        blank=False,
        validators=[validate_score],
        related_name="reviews",
        verbose_name="Оценка"
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
        blank=False,
        verbose_name="Текст комментария",
    )
    pub_date = models.DateTimeField(
        "Дата публикации комментария",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["pub_date"]

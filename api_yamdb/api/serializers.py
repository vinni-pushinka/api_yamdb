from reviews.models import Comment, Review

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment (Комментарий)."""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        # Определение связанной модели
        model = Comment
        # Определение полей модели для работы серилизатора
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review (Отзыв)."""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
        # default=serializers.CurrentUserDefault(),
    )

    class Meta:
        # Определение связанной модели
        model = Review
        # Определение полей модели для работы серилизатора
        fields = "__all__"
        # Проверка уникальности комбинации при создании подписки
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=("title", "author"),
                message="Нельзя подписаться на самого себя!",
            ),
        ]
    # REQ Пользователь может оставить только один отзыв на произведение.
    # Выбрать что-то одно:
    # - либо <validators> в <class Meta>
    # - либо <def validate>
    def validate(self, data):
        """Проверить наличие Review на Title."""
        if self.context["request"].method == "POST":
            author = self.context["view"].request.user
            title = self.context["view"].kwargs["title_id"]
            if Review.objects.filter(author=author, title_id=title).exists():
                raise serializers.ValidationError(
                    "Одно произведение - один отзыв!"
                )
        return data

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, User, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+")
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве `username` запрещено."
            )
        return value


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+")
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений основной."""

    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleReadSerializer(TitleSerializer):
    """Сериализатор произведений чтение."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор произведений запись."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )


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
        fields = "all"


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
        fields = "all"
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

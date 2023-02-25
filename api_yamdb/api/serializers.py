from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import validate_email, validate_title_year, validate_username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор Пользователей."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователей."""

    username = serializers.RegexField(
        max_length=150, regex=r"^[\w.@+-]", validators=[validate_username]
    )
    email = serializers.EmailField(max_length=254, validators=[validate_email])

    class Meta:
        model = User
        fields = ("username", "email")


class ObtainTokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения пользователем токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категорий."""

    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанров."""

    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведений основной."""

    rating = serializers.SerializerMethodField()
    year = serializers.IntegerField(validators=[validate_title_year])

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg("score", default=0))
        return rating.get("score__avg")

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
    """Сериализатор Произведений чтение."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор Произведений запись."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=False
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Отзывов."""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = SlugRelatedField(slug_field="name", read_only=True)

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    "Допустимо не более 1 отзыва на произведение"
                )
        return data

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментариев к отзывам."""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date", "review")
        read_only_fields = ("review",)

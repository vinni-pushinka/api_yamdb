from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from reviews.models import Category, Genre, Title, User, Comment, Review


class UserSerializer(serializers.ModelSerializer):
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
    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]")
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено!"
            )
        # if User.objects.filter(username=data['username']):
        #     raise serializers.ValidationError(
        #         "Использовать имя 'me' в качестве username запрещено!"
        #     )
        # if User.objects.filter(email=data['email']):
        #     raise serializers.ValidationError(
        #         "Использовать имя 'me' в качестве username запрещено!"
        #     )
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

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

    rating = serializers.SerializerMethodField()

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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review (Отзыв)."""

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
        # Определение связанной модели
        model = Review
        # Определение полей модели для работы серилизатора
        fields = ("id", "title", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment (Комментарий)."""

    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    review = serializers.ReadOnlyField(source="review.id")

    class Meta:
        # Определение связанной модели
        model = Comment
        # Определение полей модели для работы серилизатора
        fields = ("id", "text", "author", "pub_date", "review")

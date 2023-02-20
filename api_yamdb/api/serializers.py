from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+'
    )
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
    username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+'
    )
    confirmation_code = serializers.CharField(
        max_length=150
    )

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

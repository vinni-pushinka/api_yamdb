import datetime
from rest_framework import serializers
from reviews.models import (
    Category, Genre,
    Title,
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = ('slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = ('slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений при добавлении, изменении, удалении."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        year = datetime.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Указанный год не может быть больше текущего!'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализатора списка произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = ('id', 'rating')

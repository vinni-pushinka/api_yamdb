from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import CommentSerializer, ReviewSerializer
from rest_framework.pagination import LimitOffsetPagination


class CategorytViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review (Отзыв)."""

    # Указание сериализатора для валидации и сериализации
    serializer_class = ReviewSerializer
    # Ограничение доступа
    permission_classes = ()
    # Подключаем возможность пагинации
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Получить Title (Произведение) по title_id."""
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Получить набор Review (Отзыв) к Title (Произведение)."""
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создать новый Review (Отзыв) к Title (Произведение)."""
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment (Комментарий)."""

    # Указание сериализатора для валидации и сериализации
    serializer_class = CommentSerializer
    # Ограничение доступа
    permission_classes = ()
    # Подключаем возможность пагинации
    pagination_class = LimitOffsetPagination

    def get_review(self):
        """Получить Review (Отзыв) по review_id."""
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Получить набор Comment (Комментарий) к Review (Отзыву)."""
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создать новый Comment (Комментарий) к Review (Отзыву)."""
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )

from rest_framework import viewsets
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitleListSerializer
)


class CategorytViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Category (Категории)."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = ('slug')

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Genre (Жанры)."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    filterset_fields = ('slug',)
    lookup_field = ('slug')
    ordering = ('slug',)

    def get_object(self):
        return get_object_or_404(
            self.queryset, slug=self.kwargs["slug"])


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title (Произведения)."""
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer

    def list(self, request):
        queryset = self.filter_queryset(Title.objects.annotate(
            rating=Avg('reviews__score')))
        serializer = TitleListSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Title.objects.annotate(rating=Avg('reviews__score'))
        user = get_object_or_404(queryset, pk=pk)
        serializer = TitleSerializer(user)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review (Отзыв)."""

    queryset = Review.objects.all()

    # Добавить новый отзыв.
    # Пользователь может оставить только один отзыв на произведение.
    # Права доступа: **Аутентифицированные пользователи.**

    # Получить отзыв по id для указанного произведения.
    # Права доступа: **Доступно без токена.**

    # Удалить отзыв по id
    # Права доступа: **Автор отзыва, модератор или администратор.**


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment (Комментарий)."""

    queryset = Comment.objects.all()

    # Получить список всех комментариев к отзыву по id
    # Права доступа: **Доступно без токена.**

    # Добавить новый комментарий для отзыва.
    # Права доступа: **Аутентифицированные пользователи.**

    # Получить комментарий для отзыва по id.
    # Права доступа: **Доступно без токена.**

    # Частично обновить комментарий к отзыву по id.
    # Права доступа: **Автор комментария, модератор или администратор**.

    # Удалить комментарий к отзыву по id.
    # Права доступа: **Автор комментария, модератор или администратор**.

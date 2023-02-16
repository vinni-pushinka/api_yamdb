from rest_framework import viewsets

from reviews.models import Category, Comment, Genre, Review, Title


class CategorytViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review (Отзыв)."""

    # Добавить новый отзыв.
    # Пользователь может оставить только один отзыв на произведение.
    # Права доступа: **Аутентифицированные пользователи.**

    # Получить отзыв по id для указанного произведения.
    # Права доступа: **Доступно без токена.**

    # Удалить отзыв по id
    # Права доступа: **Автор отзыва, модератор или администратор.**


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment (Комментарий)."""

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

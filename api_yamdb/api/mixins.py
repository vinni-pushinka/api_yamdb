from rest_framework import mixins, viewsets


class CLDViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин модель для Жанров и Категорий."""

    pass

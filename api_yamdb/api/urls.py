from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategorytViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategorytViewSet, basename='categories')
router.register('comments', CommentViewSet, basename='comments')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]

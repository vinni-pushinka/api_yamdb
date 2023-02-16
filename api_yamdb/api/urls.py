from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategorytViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategorytViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]

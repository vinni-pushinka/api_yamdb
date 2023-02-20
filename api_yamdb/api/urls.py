from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import (
    CategorytViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    sign_up,
    obtain_token
)

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategorytViewSet, basename="categories")
router.register("comments", CommentViewSet, basename="comments")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register('users', UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", sign_up),
    path("v1/auth/token/", obtain_token),
]

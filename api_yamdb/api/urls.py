from api.views import (CategorytViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, obtain_token,
                       sign_up)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("genres", GenreViewSet, basename="genres")
router.register("categories", CategorytViewSet, basename="categories")
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/signup/", sign_up),
    path("v1/auth/token/", obtain_token),
]

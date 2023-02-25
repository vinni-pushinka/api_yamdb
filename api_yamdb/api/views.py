from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from api_yamdb.settings import EMAIL

from .filters import TitleFilter
from .mixins import CLDViewSet
from .permissions import CGTPermissions, RCPermissions, UPermissions
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ObtainTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet модели Пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UPermissions,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def my_profile(self, request):
        user = get_object_or_404(User, username=request.user.username)

        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    """Функция добавления нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get("username"), email=request.data.get("email")
    ).exists():
        user, created = User.objects.get_or_create(
            username=request.data.get("username")
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            "Код подтверждения",
            f"Здравствуйте! Новый код подтверждения: {confirmation_code}",
            EMAIL,
            [f"{request.data.get('email')}"],
            fail_silently=False,
        )
        return Response("Код подтверждения обновлён",
                        status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(
        username=request.data.get("username"), email=request.data.get("email")
    )
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(
        "Код подтверждения",
        f"Здравствуйте! Ваш код подтверждения: {confirmation_code}",
        EMAIL,
        [f"{request.data.get('email')}"],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def obtain_token(request):
    """Функция получения пользователем токена."""
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response("Неверный код подтверждения",
                        status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response(
        {"token": str(token)}, status=status.HTTP_200_OK
    )


class CategorytViewSet(CLDViewSet):
    """ViewSet модели Категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (CGTPermissions,)

    def get_object(self):
        return get_object_or_404(self.queryset, slug=self.kwargs["slug"])


class GenreViewSet(CLDViewSet):
    """ViewSet модели Жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    filterset_fields = ("slug",)
    lookup_field = "slug"
    ordering = ("slug",)
    permission_classes = (CGTPermissions,)

    def get_object(self):
        return get_object_or_404(self.queryset, slug=self.kwargs["slug"])


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet модели Произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (CGTPermissions,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели Отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (RCPermissions,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet модели Комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (RCPermissions,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

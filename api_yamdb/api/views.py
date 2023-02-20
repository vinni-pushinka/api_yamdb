from django.db.models import Avg
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from reviews.models import Category, Genre, Review, Title, User
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    UserSerializer,
    SignUpSerializer,
    ObtainTokenSerializer,
)
from api_yamdb.settings import EMAIL
from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("username",)

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def my_profile(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    email = serializer.validated_data["email"]
    new_user = User.objects.filter(username=username, email=email)
    confirmation_code = default_token_generator.make_token(new_user)
    new_user.save()
    send_mail(
        "Код подтверждения",
        f"Здравствуйте! Ваш код подтверждения: {confirmation_code}",
        EMAIL,
        [f"{email}"],
        fail_silently=False,
    )
    return Response(serializer.date, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    new_user = get_object_or_404(User, username=username)
    if confirmation_code != new_user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(new_user)
    return Response(
        {"token": str(token.access_token)}, status=status.HTTP_200_OK
    )


class CategorytViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Category (Категории)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"

    def get_object(self):
        return get_object_or_404(self.queryset, slug=self.kwargs["slug"])


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Genre (Жанры)."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    filterset_fields = ("slug",)
    lookup_field = "slug"
    ordering = ("slug",)

    def get_object(self):
        return get_object_or_404(self.queryset, slug=self.kwargs["slug"])


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title (Произведения)."""

    queryset = (
        Title.objects.all()
        .annotate(Avg("reviews__score"))
        .prefetch_related("category", "genre")
    )
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review (Отзыв)."""

    # Указание сериализатора для валидации и сериализации
    serializer_class = ReviewSerializer
    # Ограничение доступа
    permission_classes = ()

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

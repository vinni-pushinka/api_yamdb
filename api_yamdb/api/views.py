from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes

from reviews.models import Category, Comment, Genre, Review, Title, User
from api.permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from api.serializers import UserSerializer, SignUpSerializer, ObtainTokenSerializer
from api_yamdb.settings import EMAIL


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("username",)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def my_profile(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    new_user = User.objects.filter(username=username, email=email)
    confirmation_code = default_token_generator.make_token(new_user)
    new_user.save()
    send_mail(
        'Код подтверждения',
        f'Здравствуйте! Ваш код подтверждения: {confirmation_code}',
        EMAIL,
        [f'{email}'],
        fail_silently=False,
    )
    return Response(serializer.date, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    new_user = get_object_or_404(User, username=username)
    if confirmation_code != new_user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(new_user)
    return Response(
        {'token': str(token.access_token)},
        status=status.HTTP_200_OK
    )


class CategorytViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()


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

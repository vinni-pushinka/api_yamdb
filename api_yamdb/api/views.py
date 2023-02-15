from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, pagination, permissions, viewsets

from reviews.models import Category, Genre, Title


class CategorytViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

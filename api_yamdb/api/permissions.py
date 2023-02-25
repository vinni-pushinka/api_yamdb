from rest_framework import permissions


class UPermissions(permissions.BasePermission):
    """Настройка прав для Пользователей."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class CGTPermissions(permissions.BasePermission):
    """Настройка прав для Произведений, Жанров и Категорий."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        return False


class RCPermissions(permissions.BasePermission):
    """Настройка прав для Отзывов и Комментариев к ним."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

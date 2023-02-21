from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == "admin" or request.user.is_superuser:
            return True
        return False


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.role in ["moderator", "admin"]
                or request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
        return request.method in permissions.SAFE_METHODS

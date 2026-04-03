from rest_framework.permissions import BasePermission

from .models import UserProfile


def _get_role(user):
    try:
        return user.profile.role
    except UserProfile.DoesNotExist:
        return None


class IsSuperAdmin(BasePermission):
    """Full override — maps to Django is_superuser."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdmin(BasePermission):
    """Admin or Super Admin."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return _get_role(request.user) in (
            UserProfile.Role.SUPER_ADMIN,
            UserProfile.Role.ADMIN,
        )


class IsRegisteredUser(BasePermission):
    """Registered User, Admin, or Super Admin."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return _get_role(request.user) in (
            UserProfile.Role.SUPER_ADMIN,
            UserProfile.Role.ADMIN,
            UserProfile.Role.REGISTERED_USER,
        )


class IsViewer(BasePermission):
    """Any authenticated user (all roles include viewer-level access)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated
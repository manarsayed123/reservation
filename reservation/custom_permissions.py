from rest_framework.permissions import BasePermission

from authentication.models import User


class IsAdmin(BasePermission):
    """
    Allows access only to admin role.
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'role'):
            return bool(request.user and request.user.role == User.ADMIN)
        else:
            return False

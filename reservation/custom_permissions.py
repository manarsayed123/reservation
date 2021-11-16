from rest_framework.permissions import BasePermission

from authentication.models import User


class IsAdmin(BasePermission):
    """
    Allows access only to doctors.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == User.ADMIN)


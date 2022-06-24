from rest_framework.permissions import BasePermission

from apps.user.models import Role


class IsAdmin(BasePermission):
    """
    Allows access only to Vendor users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.ADMIN)


class IsExecutiveUser(BasePermission):
    """
    Allows access only to Operator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.EXECUTIVE)


class IsDealerUser(BasePermission):
    """
    Allows access only to Operator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.DEALER)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.permissions import BasePermission

from apps.user.models import Role


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.ADMIN or request.user.is_superuser)


class IsExecutiveUser(BasePermission):
    """
    Allows access only to Executive users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.EXECUTIVE)


class IsDealerUser(BasePermission):
    """
    Allows access only to Dealer users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == Role.DEALER)

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to Vendor users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == 11)


class IsOperatorUser(BasePermission):
    """
    Allows access only to Operator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.user_role == 15)

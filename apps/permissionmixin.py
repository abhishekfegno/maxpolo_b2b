from django.contrib.auth.mixins import UserPassesTestMixin

from apps.user.models import Role


class PermissionMixin(UserPassesTestMixin):
    access_to = Role.DEFAULT
    read_access = None
    write_access = None

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.read_access or self.write_access:
            if not self.write_access and not self.request.method == 'GET':
                return False
            if self.read_access > self.request.user.user_role:
                return False
        elif not self.access_to:
            raise Exception("You have to declare 'above_access' when 'read_access' or 'write_access' is not mentioned.")
        if int(self.request.user.user_role) > self.access_to:
            return False
        return True




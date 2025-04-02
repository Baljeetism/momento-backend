from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to allow only superusers to access a view.
    """

    def has_permission(self, request, view):
        if not request.user.is_superuser:
            self.message = "You must be a superuser to access this page."
            return False
        return True

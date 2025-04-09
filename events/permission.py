from rest_framework import permissions


class IsSuperUserOrEventAdminOrCreator(permissions.BasePermission):
    """
    Custom permission to allow:
    - Superusers can do anything
    - Users with `is_admin=True` can create events
    - Only the event creator or superusers can update or delete events
    """

    def has_permission(self, request, view):
        """Handles overall permission for the viewset."""
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access for everyone

        if view.action == "create":
            return request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, "is_admin", False))

        return request.user.is_authenticated  # Allow authenticated users for other actions

    def has_object_permission(self, request, view, obj):
        """Handles object-level permissions for update and delete."""
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access for everyone

        # Allow only the event creator or a superuser to modify/delete
        return request.user.is_superuser or obj.created_by == request.user
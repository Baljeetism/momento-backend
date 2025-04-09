from rest_framework import permissions

class user(permissions.BasePermission):
    """
    Custom permission to allow only superusers to access a view.
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Allow anyone to fetch reviews
        return [permissions.IsAuthenticated()]  # Require authentication for posting a review


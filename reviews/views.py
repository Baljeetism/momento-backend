from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import user

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes =[user]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.AllowAny()]  # Allow anyone to fetch reviews
    #     return [permissions.IsAuthenticated()]  # Require authentication for posting a review

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-assign the logged-in user

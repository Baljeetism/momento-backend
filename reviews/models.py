from django.db import models
# from django.contrib.auth import get_user_model
from accounts.models import User

# User = get_user_model()  # Get the user model dynamically

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    
    description = models.TextField()
   

    def __str__(self):
        return f"Review by {self.user.email}"
#this is a comment no 2
from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')  # Show user email instead of ID

    class Meta:
        model = Review
        fields = ['id', 'user', 'description']

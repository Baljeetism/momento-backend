from django.db import models
from datetime import timedelta
from django.conf import settings

# Create your models here.
class Events(models.Model):
    GENRE_CHOICES = [
        ("Music", "Music"),
        ("Sports", "Sports"),
        ("Tech", "Tech"),
        ("Art", "Art"),
        ("Food", "Food"),
        ("Comedy", "Comedy"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    duration = models.DurationField(null=True, blank=True, default=timedelta())
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    site = models.URLField(blank=True)
    venue = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    artist = models.CharField(max_length=100)
    artist_short_description = models.TextField(blank=True)
    why_attend = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events_created")
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    image_artist = models.ImageField(upload_to='artist_images/', blank=True, null=True)

    def __str__(self):
        return self.title



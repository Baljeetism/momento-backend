from django.db import models
from datetime import timedelta

# Create your models here.
class Eventsz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100)
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
    similar_events = models.ManyToManyField('self', blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)

    def __str__(self):
        return self.title
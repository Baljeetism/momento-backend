from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Attending', 'Attending'),
        ('Not_Attending', 'Not Attending'),
        ('MAYBE', 'Maybe')
        
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    event = models.ForeignKey('events.Events', on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default='Not_Attending')
    

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'RSVP'
        # verbose_name_plural = 'RSVPs'

    def __str__(self):
        return f"{self.user.username} - {self.event.name}: {self.get_status_display()}"
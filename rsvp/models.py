from django.db import models
from accounts.models import User
from events.models import Eventsz  

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Eventsz, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(max_length=20, choices=[
        ("Going", "Going"),
        ("Interested", "Interested"),
        ("Not Going", "Not Going")
    ], default="Going")
    

    class Meta:
        unique_together = ('user', 'event')  # Ensure a user can RSVP only once per event

    def __str__(self):
        return{self.user.username} 

from django.contrib import admin
from .models import RSVP

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status')
    search_fields = ('user__username', 'event__name', 'status')
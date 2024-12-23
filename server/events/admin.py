from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['description', 'start', 'end', 'creator', 'get_participants', 'created_at', 'update_at', 'active']

    def get_participants(self, obj):
        return ", ".join([participant.name for participant in obj.participants.all()])
    get_participants.short_description = 'Participants'

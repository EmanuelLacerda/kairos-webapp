from django.contrib import admin
from .models import User, Event

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = {'name', 'email', 'created_at', 'update_at', 'active'}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = {'description', 'start', 'end', 'creator', 'participants', 'created_at', 'update_at', 'active'}
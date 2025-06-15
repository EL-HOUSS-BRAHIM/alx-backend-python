from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'seen', 'timestamp']
    list_filter = ['seen']
    search_fields = ['user__username', 'message__content']

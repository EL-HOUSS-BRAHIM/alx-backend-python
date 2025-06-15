from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')
    readonly_fields = ('message_id', 'timestamp')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Message Information', {
            'fields': ('message_id', 'sender', 'receiver', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'timestamp')
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at', 'user')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('notification_id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('notification_id', 'user', 'message', 'notification_type')
        }),
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    ) 
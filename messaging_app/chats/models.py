from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """
    Extended User model with additional fields for messaging functionality.
    Inherits all fields from AbstractUser including: username, first_name, last_name, 
    email, password, is_staff, is_active, date_joined, etc.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
      # Note: password field is inherited from AbstractUser
    # password = models.CharField(max_length=128)  # Inherited from AbstractUser
    # Other inherited fields: username, first_name, last_name, email, is_staff, 
    # is_active, is_superuser, last_login, date_joined, groups, user_permissions
    
    # Override username to make email the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'chats_user'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chats_conversation'
        ordering = ['-updated_at']
        
    def __str__(self):
        participant_names = ", ".join([str(user) for user in self.participants.all()[:2]])
        if self.participants.count() > 2:
            participant_names += f" and {self.participants.count() - 2} others"
        return f"Conversation: {participant_names}"


class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chats_message'
        ordering = ['sent_at']
        
    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

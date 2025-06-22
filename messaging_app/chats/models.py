import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=128)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(
            Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username}: {self.message_body[:30]}"

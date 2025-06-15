from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager



class Message(models.Model):
    objects = models.Manager()        # Manager par défaut
    unread = UnreadMessagesManager()  # 👈 Manager personnalisé
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Indicate if the message was edited
    edited_at = models.DateTimeField(null=True, blank=True)  # The timestamp when the message was edited
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)  # The user who edited the message
    # 🔁 Pour les threads : réponse à un autre message
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)


    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp} and {self.sender} -> {self.receiver}: {self.content[:20]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} regarding message {self.message.id}"


# messaging/models.py
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id}: {self.old_content[:20]}"

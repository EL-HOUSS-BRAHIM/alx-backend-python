# messaging/managers.py

from django.db import models

# class UnreadMessagesManager(models.Manager):
#     def unread_for_user(self, user):
#         return self.filter(receiver=user, read=False).only('id', 'content', 'sender_id')


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')

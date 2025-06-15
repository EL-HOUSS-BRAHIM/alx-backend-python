from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils import timezone
from .models import Message


class NotificationTestCase(TestCase):
    
    def setUp(self):
        # Creating two users
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

    def test_notification_creation(self):
        # Send a message from sender to receiver
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message!"
        )
        
        # Check if a notification has been created for the receiver
        notification = Notification.objects.filter(user=self.receiver, message=message).exists()
        self.assertTrue(notification)
        
    def test_no_notification_for_non_receiver(self):
        # Send a message from sender to receiver
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Another test message!"
        )
        
        # Check that no notification is created for the sender
        notification = Notification.objects.filter(user=self.sender, message=message).exists()
        self.assertFalse(notification)


class MessageTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_message_edit(self):
        # Create a message
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello!")
        
        # Edit the message
        message.content = "Hello, how are you?"
        message.save()

        # Fetch the message again and check if it was edited
        message.refresh_from_db()

        # Check that the edited fields were updated
        self.assertTrue(message.edited)
        self.assertEqual(message.edited_by, self.user1)  # The user who edited the message
        self.assertTrue(message.edited_at <= timezone.now())  # The timestamp should be current or before now

        # Check if the message history was created
        history = MessageHistory.objects.filter(message=message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Hello!")


class ThreadedMessageTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='password')
        self.user2 = User.objects.create_user(username='bob', password='password')

        # Message racine
        self.root = Message.objects.create(sender=self.user1, receiver=self.user2, content="Message principal")

        # Réponse directe
        self.reply1 = Message.objects.create(sender=self.user2, receiver=self.user1, content="Réponse 1", parent_message=self.root)

        # Réponse à une réponse
        self.reply2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Réponse 1.1", parent_message=self.reply1)

    def test_thread_structure(self):
        # Le message racine ne doit pas avoir de parent
        self.assertIsNone(self.root.parent_message)

        # Le message root doit avoir 1 réponse directe
        self.assertEqual(self.root.replies.count(), 1)
        self.assertIn(self.reply1, self.root.replies.all())

        # La première réponse a aussi une réponse
        self.assertEqual(self.reply1.replies.count(), 1)
        self.assertIn(self.reply2, self.reply1.replies.all())

        # Le dernier message n’a pas de réponse
        self.assertEqual(self.reply2.replies.count(), 0)


def test_unread_manager(self):
    unread = Message.unread.for_user(self.user2)
    self.assertIn(self.msg_unread, unread)
    self.assertNotIn(self.msg_read, unread)

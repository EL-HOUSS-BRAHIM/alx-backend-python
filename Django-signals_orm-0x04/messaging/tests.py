from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

User = get_user_model()

class MessagingModelsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_message_creation(self):
        """Test creating a message"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, this is a test message!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.receiver, self.user2)
        self.assertEqual(message.content, 'Hello, this is a test message!')
        self.assertFalse(message.is_read)
        self.assertIsNotNone(message.message_id)
        self.assertIsNotNone(message.timestamp)
    
    def test_notification_creation(self):
        """Test creating a notification"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message for notification'
        )
        
        notification = Notification.objects.create(
            user=self.user2,
            message=message,
            notification_type='message',
            title='New message from testuser1',
            content='You have received a new message'
        )
        
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'message')
        self.assertFalse(notification.is_read)
        self.assertIsNotNone(notification.notification_id)
        self.assertIsNotNone(notification.created_at)

class MessagingSignalsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_message_notification_signal(self):
        """Test that creating a message automatically creates a notification"""
        # Count initial notifications
        initial_count = Notification.objects.count()
        
        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='This should trigger a notification'
        )
        
        # Check that a notification was created
        self.assertEqual(Notification.objects.count(), initial_count + 1)
        
        # Get the created notification
        notification = Notification.objects.get(user=self.user2, message=message)
        
        # Verify notification details
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertEqual(notification.notification_type, 'message')
        self.assertIn('testuser1', notification.title)
        self.assertIn('This should trigger a notification', notification.content)
        self.assertFalse(notification.is_read)
    
    def test_message_read_notification_update(self):
        """Test that marking a message as read updates the notification"""
        # Create a message (which creates a notification)
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message for read status'
        )
        
        # Get the notification
        notification = Notification.objects.get(user=self.user2, message=message)
        self.assertFalse(notification.is_read)
        
        # Mark message as read
        message.is_read = True
        message.save()
        
        # Refresh notification from database
        notification.refresh_from_db()
        
        # Check that notification is now marked as read
        self.assertTrue(notification.is_read)
    
    def test_multiple_messages_multiple_notifications(self):
        """Test that multiple messages create multiple notifications"""
        # Create multiple messages
        for i in range(3):
            Message.objects.create(
                sender=self.user1,
                receiver=self.user2,
                content=f'Message {i + 1}'
            )
        
        # Check that 3 notifications were created
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 3)
        
        # Verify each notification has correct content
        notifications = Notification.objects.filter(user=self.user2).order_by('created_at')
        for i, notification in enumerate(notifications):
            self.assertIn(f'Message {i + 1}', notification.content)

class MessagingModelMethodsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@test.com',
            password='testpass123'
        )
    
    def test_message_str_method(self):
        """Test Message __str__ method"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        expected_str = f"Message from {self.user1.username} to {self.user2.username} at {message.timestamp}"
        self.assertEqual(str(message), expected_str)
    
    def test_notification_str_method(self):
        """Test Notification __str__ method"""
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        
        notification = Notification.objects.create(
            user=self.user2,
            message=message,
            notification_type='message',
            title='Test notification',
            content='Test content'
        )
        
        expected_str = f"Notification for {self.user2.username}: Test notification"
        self.assertEqual(str(notification), expected_str) 
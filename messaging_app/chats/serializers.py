from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user instance, handling password separately"""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested relationships (without sensitive data)"""
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserBasicSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'conversation',
            'message_body', 'sent_at'
        ]
        extra_kwargs = {
            'message_id': {'read_only': True},
            'sent_at': {'read_only': True},
        }
    
    def validate_sender_id(self, value):
        """Validate that the sender exists"""
        try:
            User.objects.get(user_id=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid sender ID")


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating messages (simplified)"""
    
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages"""
    participants = UserBasicSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids',
            'created_at', 'messages', 'message_count', 'last_message'
        ]
        extra_kwargs = {
            'conversation_id': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def get_message_count(self, obj):
        """Get the total number of messages in the conversation"""
        return obj.messages.count()
    
    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def create(self, validated_data):
        """Create a conversation with participants"""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation
    
    def validate_participant_ids(self, value):
        """Validate that all participant IDs exist"""
        if value:
            existing_users = User.objects.filter(user_id__in=value)
            if len(existing_users) != len(value):
                raise serializers.ValidationError("One or more participant IDs are invalid")
        return value


class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for conversation list view"""
    participants = UserBasicSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'created_at',
            'message_count', 'last_message'
        ]
    
    def get_message_count(self, obj):
        """Get the total number of messages in the conversation"""
        return obj.messages.count()
    
    def get_last_message(self, obj):
        """Get basic info about the last message"""
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'message_body': last_message.message_body[:50] + '...' if len(last_message.message_body) > 50 else last_message.message_body,
                'sender': last_message.sender.username,
                'sent_at': last_message.sent_at
            }
        return None


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating conversations"""
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids']
    
    def validate_participant_ids(self, value):
        """Validate participant IDs and ensure they exist"""
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        
        existing_users = User.objects.filter(user_id__in=value)
        if len(existing_users) != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid")
        
        return value
    
    def create(self, validated_data):
        """Create conversation with participants"""
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create()
        
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        
        return conversation

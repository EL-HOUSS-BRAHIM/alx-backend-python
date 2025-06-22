from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['user_id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id',
                  'sender',
                  'sender_username',
                  'conversation',
                  'message_body',
                  'sent_at']

    def get_sender_username(self, obj):
        return obj.sender.username

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

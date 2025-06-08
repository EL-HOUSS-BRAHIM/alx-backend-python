from rest_framework import serializers
from .models import User, Conversation, Message

class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    last_name = serializers.CharField(blank=True, required=False)

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number', 'full_name')

    def get_full_name(self, obj):
        """
        Return the full name of the user.
        `obj` here refers to the User instance being serialized
        """
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with a '+' sign")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    # For full user detail like your own profile
    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number',
                  'is_staff', 'is_active', 'date_joined', 'last_login')

class ConversationSerializer(serializers.ModelSerializer):
    # for READ operations: showing nested user details
    participants = UserListSerializer(read_only=True, many=True)

    # for WRITE operations: accepting participant IDs
    # might pass participants_id in the request body for creating a conversation
    participants_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True, # field is only for writing
        source='participants' # mapping to participant's ManyToManyFIeld
    )

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants', 'participants_ids', 'created_at')

class MessageSerializer(serializers.ModelSerializer):
    # For displaying sender's full details on read operations
    sender = UserListSerializer(read_only=True)
    
    # For accepting sender's ID on read operations
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='sender' # Map to 'sender' ForeignKey
    )

    # For displaying conversation's full details on read operations
    conversation = ConversationSerializer(read_only=True)

    # For accepting conversation's ID on read operations
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        write_only=True,
        source='conversation' # Map to 'conversation' ForeignKey
    )


    class Meta:
        model = Message
        fields = ('message_id', 'message_body', 'sent_at', 'created_at',
                  'sender', 'sender_id', 'conversation', 'conversation_id')

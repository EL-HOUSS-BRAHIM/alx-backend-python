from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken


class UserListSerializer(serializers.ModelSerializer):
    # For listing/nesting info without sensitive info
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone_number', 'username', 'full_name')

    def get_full_name(self, obj):
        """
        Return the full name of the user.
        `obj` here refers to the User instance being serialized
        """
        if obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        else:
            return f"{obj.first_name}"
    
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
        
        read_only_fields = ('user_id', 'data_joined', 'last_login', 'is_staff',
                            'is_active')

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
        read_only_fields = ('conversation_id', 'created_at')

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants_data)
        return conversation
    
    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants', None)
        if participants_data is not None:
            instance.participants.set(participants_data)

        instance.created_at = validated_data.get('created_at', instance.created_at)

        instance.save()
        return instance


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
    conversation = serializers.StringRelatedField(read_only=True)

    # For accepting conversation's ID on read operations
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        write_only=True,
        source='conversation' # Map to 'conversation' ForeignKey
    )


    class Meta:
        model = Message
        fields = ('message_id', 'message_body', 'edited_at', 'created_at',
                  'sender', 'sender_id', 'conversation', 'conversation_id')
        read_only_fields = ('message_id', 'created_at', 'sender', 'conversation')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.name
        return token
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Conversation, Message

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_permission(self, request, view):
        """
        Return True if the user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow participants of a conversation
        to access related objects (messages, conversation details).
        """
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        elif hasattr(obj, 'participants'):
            conversation = obj
        else:
            return False
        
        # Allow safe methods (GET, HEAD, OPTIONS) and modifying methods (PUT, PATCH, DELETE) for participants
        if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH', 'DELETE']:
            return conversation.participants.filter(user_id=request.user.user_id).exists()
        
        # Allow POST for participants (e.g., sending messages)
        return conversation.participants.filter(user_id=request.user.user_id).exists()

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False

class IsParticipantOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        elif hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False

class IsMessageSender(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Allow participants to view messages, but only the sender can modify (PUT, PATCH, DELETE).
        """
        if request.method in permissions.SAFE_METHODS:
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        return False

class IsConversationParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(user_id=request.user.user_id).exists()

class CanModifyConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.participants.filter(user_id=request.user.user_id).exists():
            return False
        return True

class IsUserSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'user_id') and obj == request.user:
            return True
        return False

class CanAccessUserData(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            from django.db.models import Q
            shared_conversations = Conversation.objects.filter(
                Q(participants=request.user) & Q(participants=obj)
            ).exists()
            return shared_conversations
        return False

class IsOwnerOrParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        elif hasattr(obj, 'author') and obj.author == request.user:
            return True
        elif hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        if hasattr(obj, 'participants'):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        return False

class ReadOnlyForNonParticipants(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_participant = False
        if hasattr(obj, 'participants'):
            is_participant = obj.participants.filter(user_id=request.user.user_id).exists()
        elif hasattr(obj, 'conversation'):
            is_participant = obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        if is_participant:
            return True
        return request.method in permissions.SAFE_METHODS

class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False
    def has_object_permission(self, request, view, obj):
        return False

class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True
    def has_object_permission(self, request, view, obj):
        return True

class IsParticipantOfConversationForList(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        conversation_id = view.kwargs.get('conversation_id') or view.kwargs.get('conversation_pk')
        if not conversation_id:
            conversation_id = request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
                return conversation.participants.filter(user_id=request.user.user_id).exists()
            except (Conversation.DoesNotExist, ValueError):
                return False
        return True

class IsMessageAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'sender'):
            return obj.sender == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class CanCreateMessage(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method == 'POST':
            conversation_id = request.data.get('conversation') or view.kwargs.get('conversation_id')
            if conversation_id:
                try:
                    conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
                    return conversation.participants.filter(user_id=request.user.user_id).exists()
                except (Conversation.DoesNotExist, ValueError):
                    return False
        return True
from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to:
    - View messages (GET)
    - Send messages (POST)
    - Update messages (PUT/PATCH)
    - Delete messages (DELETE)
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if view.action in ['list', 'create']:
            return True
            
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
            
        elif isinstance(obj, Message):
            # For safe methods (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return obj.conversation.participants.filter(id=request.user.id).exists()
            
            return (
                obj.sender == request.user or  # User is the sender
                obj.conversation.participants.filter(id=request.user.id).exists()  # User is participant
            )
            
        return False

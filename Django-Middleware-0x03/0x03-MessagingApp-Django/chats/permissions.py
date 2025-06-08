from rest_framework import permissions


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Allow only participants in a conversation to send, 
    view, update and delete messages
    Read-only access is allowed for authenticated user.
    """
    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        # GET, HEAD, OPTIONS are allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowd to sender of message.
        # can perform POST, PUT, PATCH and DELETE
        # 'obj' is the Message instance and 'obj.sender' is the User instance
        return obj.sender == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the api/view, manage conversation
    """

    def has_object_permission(self, request, view, obj):
        # 'obj' is the Conversation instance
        return request.user in obj.participants.all()
    
    def has_permission(self, request, view):
        # For list view, ensure user is authenticated
        return request.user and request.user.is_authenticated

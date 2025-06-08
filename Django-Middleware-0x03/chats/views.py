from rest_framework import viewsets, permissions, serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .pagination import CustomPagination
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from .permissions import IsParticipantOfConversation, IsSenderOrReadOnly

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing conversations and listing conversations
    for authenticated users.
    """
    serializer_class = ConversationSerializer
    authentication_class = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        """
        Ensures a user only sees conversations they are a participant of
        """
        if self.request.user.is_authenticated:
            return self.request.user.conversations.all().distinct()
        return Conversation.objects.none()
    
    def perform_create(self, serializer):
        """
        add the creating user as a participant if not explicity provided
        """
        participants_from_request = serializer.validated_data.get('participants', [])
        if self.request.user not in participants_from_request:
            participants_from_request.append(self.request.user)

        serializer.save(participants=participants_from_request)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing messages
    """
    serializer_class = MessageSerializer
    authentication_class = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsSenderOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Filter messages to only those within a conversation the current user is part of
        """
        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        conversation_pk = self.kwargs.get('conversation_pk')

        if not conversation_pk:
            user_conversations = self.request.user.conversation.all()
            return Message.objects.filter(
                conversation__in=user_conversations
                ).select_related('sender', 'conversation').order_by('created_at')
        
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_pk,
                participants=self.request.user
            )
        except Conversation.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND('Conversation not found or you are not a participant.')
        
        return Message.objects.filter(
            conversation=conversation
            ).select_related('sender', 'conversation').order_by('created_at')
    
    def perform_create(self, serializer):
        """
        Automatically assign authenticated user as sender.
        Ensure message is for a conversation the user is part of.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if not conversation_pk:
            raise serializers.ValidationError(
                {"conversation_pk": "Conversation ID must be provided in the URL path."}
                )
        try:
            # Verify user is a participant of the conversation
            conversation = Conversation.objects.get(
                conversation_id=conversation_pk,
                participants=self.request.user
            )
        except Conversation.DoesNotExist:
            raise permissions.PermissionDenied(
                {"Invalid conversation ID or you are not a participant of this conversation"}
            )
        
        serializer.save(sender=self.request.user, conversation=conversation)

    def perform_update(self, serializer):
        """
        Prevents users from changing sender or conversation of existing messages.
        Ensures only the sender can update their own message
        """
        if serializer.instance.sender != self.request.user:
            raise permissions.PermissionDenied("You cannot update messages sent by others")

        # prevent users from changing the sender or conversation of existing messages
        if 'conversation' in serializer.validated_data and \
            serializer.validated_data['conversation'] != serializer.instance.conversation:
            raise permissions.PermissionDenied("You cannot change the conversation of a message.")
        
        if 'conversation' in serializer.validated_data and \
            serializer.validated_data['sender'] != serializer.instance.sender:
            raise permissions.PermissionDenied("You cannot change the sender of a message.")

        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensures only the sender can delete their own message
        """
        if instance.sender != self.request.user:
            raise permissions.PermissionDenied("You are not allowed to delete messages sent by others.")
        instance.delete()


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": str(e)})
        
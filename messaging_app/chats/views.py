from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from .pagination import MessagePagination
from .filters import MessageFilter
import django_filters
from django.db.models import Q
from rest_framework import status

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        
        if request.user.id not in participants:
            participants.append(request.user.id)
            
        if len(participants) < 2:
            return Response(
                {"error": "At least two participants are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    search_fields = ['content']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied(
                {"error": "You're not a participant of this conversation"},
                code=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        message = self.get_object()
        if message.sender != self.request.user:
            raise PermissionDenied(
                {"error": "You can only edit your own messages"},
                code=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if (instance.sender != self.request.user and 
            not instance.conversation.participants.filter(id=self.request.user.id).exists()):
            raise PermissionDenied(
                {"error": "You don't have permission to delete this message"},
                code=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                exc.detail,
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)

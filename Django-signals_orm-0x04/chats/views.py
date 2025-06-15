from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, MessageSerializer,
    MessageBasicSerializer, ConversationSerializer
)
from .pagination import StandardResultsSetPagination

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related('participants', 'messages').order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='add-participant')
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get("user_id")
        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response({"error": "User not found."}, status=404)
        conversation.participants.add(user)
        return Response({"message": f"{user.username} added."})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user).select_related('sender', 'conversation')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

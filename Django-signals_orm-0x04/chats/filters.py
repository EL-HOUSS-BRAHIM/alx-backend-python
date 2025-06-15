import django_filters as filters
from chats.models import Message
import uuid

class MessageFilter(filters.FilterSet):
    """
    Filter class for messages, allowing filtering by sender, conversation participants, and time range.
    """
    sender_id = filters.UUIDFilter(field_name='sender__user_id')
    participant_id = filters.UUIDFilter(field_name='conversation__participants__user_id')
    sent_at__gte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_id', 'participant_id', 'sent_at__gte', 'sent_at__lte']
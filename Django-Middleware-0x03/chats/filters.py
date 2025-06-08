import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    from_this_time = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    to_this_time = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')

    sender = django_filters.CharFilter(field_name="sender", lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender', 'created_at']
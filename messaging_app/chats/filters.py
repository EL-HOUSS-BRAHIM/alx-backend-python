import django_filters
from .models import Message
from django.utils import timezone
from datetime import timedelta

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username')
    conversation = django_filters.NumberFilter(field_name='conversation__id')
    start_date = django_filters.DateTimeFilter(
        field_name='sent_at', 
        lookup_expr='gte'
    )
    end_date = django_filters.DateTimeFilter(
        field_name='sent_at', 
        lookup_expr='lte'
    )
    last_24_hours = django_filters.BooleanFilter(
        method='filter_last_24_hours',
        label='Messages from last 24 hours'
    )

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']

    def filter_last_24_hours(self, queryset, name, value):
        if value:
            return queryset.filter(
                sent_at__gte=timezone.now() - timedelta(hours=24)
            )
        return queryset

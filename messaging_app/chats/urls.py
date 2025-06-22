from django.urls import path, include
from rest_framework import routers  # <-- includes DefaultRouter()
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

default_router = routers.DefaultRouter()
default_router.register(r'conversations', ConversationViewSet, basename='conversation')

nested_router = NestedDefaultRouter(default_router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(nested_router.urls)),
]


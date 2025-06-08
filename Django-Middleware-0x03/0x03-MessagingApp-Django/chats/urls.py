from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# Registering messages as a nested ressource
conversations_router.register(r'messages', MessageViewSet, basename='conversation-message')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
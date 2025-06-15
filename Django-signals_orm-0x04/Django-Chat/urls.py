# Django-Chat/urls.py
from django.urls import path
from . import views
from .views import delete_user

urlpatterns = [
    path('message/<int:message_id>/history/', views.message_history_view, name='message-history'),
    path('delete-account/', delete_user, name='delete_user'),

]

# Django-Chat/views.py
from django.shortcuts import render
from messaging.models import Message, MessageHistory
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout




def message_history_view(request, message_id):
    message = Message.objects.get(id=message_id)
    history = MessageHistory.objects.filter(message=message)
    return render(request, 'chat/message_history.html', {'message': message, 'history': history})

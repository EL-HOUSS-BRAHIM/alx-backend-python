from django.shortcuts import redirect, render
from messaging.models import Message
from .helpers import get_thread
# from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout


@login_required
def delete_user(request):
    user = request.user
    logout(request) 
    user.delete()
    return redirect('login')


# def conversation_thread(request):
#     # On récupère tous les messages racines
#     messages = Message.objects.filter(parent_message__isnull=True).select_related('sender', 'receiver').prefetch_related(
#         Prefetch('replies', queryset=Message.objects.select_related('sender'))
#     )
#     return render(request, 'messages/thread.html', {'messages': messages})

def threaded_conversation_view(request):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    return render(request, 'messaging/thread.html', {'messages': messages})


def view_message_thread(request, message_id):
    root = Message.objects.select_related('sender', 'receiver').get(id=message_id)
    thread = get_thread(root)
    return render(request, 'messages/thread_detail.html', {'message': root, 'thread': thread})


# @login_required
# def unread_messages_view(request):
#     sender = request.user
#     unread_msgs = Message.unread.for_user(sender)
#     return render(request, 'messages/unread.html', {'messages': unread_msgs})

@login_required
def user_messages_view(request):
    messages = Message.objects.filter(sender=request.user)\
        .select_related('receiver')\
        .prefetch_related('history', 'replies')  # Assuming Message has related_name="replies"

    return render(request, 'messaging/user_messages.html', {'messages': messages})

# Par exemple, ta vue qui affiche la liste des messages d'une conversation :
@cache_page(60)  # 60 secondes de cache
def conversation_messages(request, conversation_id):
    # logique pour récupérer messages
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
    return render(request, 'messaging/conversation.html', {'messages': messages})

def unread_messages_view(request):
    unread = Message.unread.unread_for_user(request.user).only(
        'id', 'content', 'sender', 'timestamp'
    )
    return render(request, 'messaging/unread.html', {'unread_messages': unread})

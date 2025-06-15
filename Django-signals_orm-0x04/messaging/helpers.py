# helpers.py

def get_thread(message):
    """
    Récupère un message + toutes ses réponses récursivement
    """
    replies = list(message.replies.all())
    for reply in replies:
        reply.replies_recursive = get_thread(reply)
    return replies

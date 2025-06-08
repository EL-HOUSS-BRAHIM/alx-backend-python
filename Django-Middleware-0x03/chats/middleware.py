from datetime import datetime, time
import os
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from time import sleep
import asyncio


class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        log_file_path = os.path.join(parent_dir, 'requests.log')

        with open(log_file_path, 'a') as log_file:
            log = f"\n{datetime.now()} - User: {request.user} - Path: {request.path}"
            log_file.write(log)
        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        to_time = time(21, 0, 0)
        from_time = time(18, 0, 0)

        if from_time <= current_time <= to_time:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        if ip not in self.message_count:
            self.message_count[ip] = 0
            response = self.get_response(request)
            return response

        elif self.message_count[ip] == 5:
            print(
                f"User: {request.user} with IP: {ip} won't send any new message for 1 minute"
                )
            
            sleep(60)

            del self.message_count[ip]

            response = Response(
                data='You have been limited due to sending too many messages',
                status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            return response
        
        elif request.method == 'POST':
            self.message_count[ip] += 1
            print(f"User: {request.user} with IP: {ip} has sent {self.message_count[ip]} messages")
            
        response = self.get_response(request)
        return response
    

class RolepermissionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)
        return response
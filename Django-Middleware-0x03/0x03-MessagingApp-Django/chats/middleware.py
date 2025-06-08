from datetime import datetime
import os


class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        log_file_path = os.path.join(parent_dir, 'requests.log')

        with open(log_file_path, 'a') as log_file:
            log = f"\n{datetime.now()} - User: {request.user} - Path: {request.path}"
            print(log)
            log_file.write(log)
        response = self.get_response(request)
        return response
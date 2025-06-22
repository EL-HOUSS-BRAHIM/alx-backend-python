from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenAuthentication(authentication.BaseAuthentication):
    """
    Custom token-based authentication.
    Clients should authenticate by passing the token in the "X-Custom-Token" header.
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_X_CUSTOM_TOKEN', '').strip()
        
        if not auth_header:
            return None  # No token provided
        
        try:
            # Example: Validate your custom token format
            if not auth_header.startswith('CustomToken '):
                raise exceptions.AuthenticationFailed('Invalid token format')
                
            token = auth_header.split(' ')[1]
            
            # Example: Look up user by token (you'd need a model that stores these)
            user = User.objects.get(auth_token__key=token)
            
            return (user, token)  # Authentication successful
            
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

from .models import User, UserSession
from django.contrib.auth.backends import ModelBackend

class SessionTokenAuthBackend(ModelBackend):
    """
        Validation backend
    """

    def authenticate(self, request=None, session_token=None, **kwargs):
        if session_token:
            try:
                return UserSession.objects.get(session_token=session_token).user
            except UserSession.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
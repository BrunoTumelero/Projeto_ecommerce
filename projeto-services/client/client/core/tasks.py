from django.conf import settings
from django.utils import timezone

from client.register.models import UserSession
from datetime import timedelta

def eliminate_token_session():
    time = timezone.now() - timedelta(days=2)
    token_session = UserSession.objects.filter(created_at__lt=time)
    token_session.delete()
    
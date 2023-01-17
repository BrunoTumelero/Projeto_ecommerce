import hashlib
import time
import random

from client.register.models import *

def _create_token(user):
    random.seed()
    cod = hashlib.md5()
    cod.update((str(random.randint(0, 100000000000)) +
                str(time.time())).encode("utf-8"))
    session_token = cod.hexdigest()
    user_session = UserSession(user=user, session_token=session_token)
    user_session.save()
    return session_token
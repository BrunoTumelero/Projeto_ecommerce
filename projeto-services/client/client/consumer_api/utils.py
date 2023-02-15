import hashlib
import time
import random
import string

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

def _create_activation_token():
    cod = string.ascii_letters + string.digits
    len_cod = random.randint(5, 20)
    key = ''.join(random.choice(cod) for _ in range(len_cod))
    return str(key)
    
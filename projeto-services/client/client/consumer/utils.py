import hashlib
import time
import random
import requests
import base64

from client.register.models import *
from gerencianet import Gerencianet
from django.conf import settings

def _create_token(user):
    random.seed()
    cod = hashlib.md5()
    cod.update((str(random.randint(0, 100000000000)) +
                str(time.time())).encode("utf-8"))
    session_token = cod.hexdigest()
    user_session = UserSession(user=user, session_token=session_token)
    user_session.save()
    return session_token

def generate_key_pix():
    gn = Gerencianet(settings.CREDENCIAIS)

    response =  gn.pix_create_evp()
    return response

def token_verification_payment():
    credentials = {
    "client_id": settings.DEV_CLIENT_KEY,
    "client_secret": settings.DEV_SECRET_KEY,
}

    certificado = f'client/credinciais/{settings.CERT_DEV}'  # A variável certificado é o diretório em que seu certificado em formato .pem deve ser inserido

    auth = base64.b64encode(
        (f"{credentials['client_id']}:{credentials['client_secret']}"
        ).encode()).decode()

    url = "https://api-pix-h.gerencianet.com.br/oauth/token"  #Para ambiente de Desenvolvimento

    payload="{\r\n    \"grant_type\": \"client_credentials\"\r\n}"
    headers = {
        'Authorization': f"Basic {auth}",
        'Content-Type': 'application/json'
    }

    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=payload,
                                cert=certificado)

    return response.text
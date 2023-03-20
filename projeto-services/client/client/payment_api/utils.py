import requests
import base64
import json
import string
import random

from gerencianet import Gerencianet
from django.conf import settings

from client.register.models import Pix


def get_token_api_payment():
    credentials = {
    "client_id": settings.DEV_CLIENT_KEY,
    "client_secret": settings.DEV_SECRET_KEY,
}

    certificado = f'client/payment_api/certificates/{settings.CERT_DEV}'  # A variável certificado é o diretório em que seu certificado em formato .pem deve ser inserido
    
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
    access = response.json()

    return access['access_token']

def _headers():
    heraders = {
        'Authorization': f'Bearer {get_token_api_payment()}',
        'Content-Type': 'application/json'
    }
    return heraders

def generate_key_pix():
    print('Gerando chave...')

    certificado = f'{settings.PATH_CREDENTIALS}{settings.CERT_DEV}'

    url = "https://api-pix-h.gerencianet.com.br/v2/gn/evp"

    payload={}
    headers = {
        'authorization': f'Bearer {get_token_api_payment()}',
        #'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cert=certificado)
    print(response)

    return response.json()

def txid_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def validation_gn_keys():
    options = {
    'client_id': settings.DEV_CLIENT_KEY,
    'client_secret': settings.DEV_SECRET_KEY,
    'sandbox': True
    }
    return options

def save_pix(response: json, payer, receiver):
    if Pix.objects.filter(txid=response.txid).exists():
        try:
            pix = Pix.objects.get(txid=response.txid)
        except Pix.MultipleObjectsReturned:
            return json({'message': 'Erro no identificador do pix', 'status': 404})
    else:
        pix = Pix.objects.update_or_create(txid=response.txid)
        pix.value = response.valor.original
        pix.time = response.calendario.criacao
        pix.payer_id = payer
        pix.receiver_id = receiver
        pix.return_pix_id = False
        pix.save()
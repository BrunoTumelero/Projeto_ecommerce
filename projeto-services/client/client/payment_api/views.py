from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse

import requests
import base64
import json

from client.public_api.decorators import user_authenticate
from .utils import _headers, get_token_api_payment
from client.register.models import Shopping_Cart

@csrf_exempt
@user_authenticate
def pix_payment(request):
    value_purchases = Shopping_Cart.objects.filter(consumer=request.user.pk)
    total_item = [item.total for item in value_purchases]
    total_pushased = sum(total_item)

    headers = _headers()
    certificado = f'client/payment_api/certificates/{settings.CERT_DEV}'

    url = f'{settings.GN_BASE_URL}/v2/cob'
    payload = json.dumps({
    "calendario": {
        "expiracao": 3600
    },
    "devedor": {
        "cpf": request.user.consumer_name.cpf,
        "nome": request.user.consumer_name.full_name
    },
    "valor": {
        "original": str(total_pushased)
    },
    "chave": "03659197050",
    "solicitacaoPagador": "Informe o número ou identificador do pedido.",
    "infoAdicionais": [
        {
        "nome": "Campo 1",
        "valor": "Informação Adicional1 do PSP-Recebedor"
        },
        {
        "nome": "Campo 2",
        "valor": "Informação Adicional2 do PSP-Recebedor"
        }
    ]
    })

    response = requests.request("POST", url, headers=headers, data=payload, cert=certificado)

    return JsonResponse({'message': response.json()})
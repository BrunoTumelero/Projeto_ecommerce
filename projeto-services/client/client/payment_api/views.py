from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

import requests
import base64
import json

from client.public_api.decorators import user_authenticate, company_autentication
from .utils import _headers, txid_generator, generate_key_pix
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
    "chave": "e63a6451-ec39-450a-aaac-6310baaa25e7",
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

    return JsonResponse({'response': response.json()})

@csrf_exempt
@user_authenticate
@company_autentication
def generate_qr_code(request):
    loc_id = request.POST.get('loc_id', None)

    headers = _headers()
    certificate = f'{settings.PATH_CREDENTIALS}{settings.CERT_DEV}'

    if loc_id:
        url = url = f"{settings.GN_BASE_URL}/v2/loc/{loc_id}/qrcode"
    else:
        return JsonResponse({'message': 'Informe o id de localização da cobrança', 'status': 404})

    response = requests.request("GET", url, headers=headers, data={}, cert=certificate)
    qrcode = response.json()

    return JsonResponse({'response': qrcode['imagemQrcode']})

@csrf_exempt
@user_authenticate
@company_autentication
def get_pix_bilings(request):
    start_date = request.POST.get('start_date', None) #timezone
    end_date = request.POST.get('end_date', None)
    cpf = request.POST.get('cpf', None)
    cnpj = request.POST.get('cnpj', None)
    status = request.POST.get('status', None)
    pag = request.POST.get('pag', 1)
    items_pag = request.POST.get('items_pag', 20)

    headers = _headers()
    certificado = f'{settings.PATH_CREDENTIALS}{settings.CERT_DEV}'
    
    if start_date and end_date:
        start_date += 'T00:00:00.000Z'
        end_date += 'T00:00:00.000Z'
    else:
        return JsonResponse({'message': 'Informe a data', 'status': 404})

    if start_date and end_date:
        url = f'{settings.GN_BASE_URL}/v2/pix?inicio={start_date}&fim={end_date}'
    if cpf:
        url += f'&cpf={cpf}'
    if cnpj:
        url += f'&cnpj={cnpj}'
    if status:
        url += f'&status={status.upper()}'
    if pag:
        url += f'&paginacao.paginaAtual={pag}'
    if items_pag:
        url += f'&paginacao.itensPorPagina={pag}'

    payload = {}
    
    response = requests.request("GET", url, headers=headers, data=payload, cert=certificado)

    return JsonResponse({
        'message': response.json(),
        'status': 200
    })

@csrf_exempt
@user_authenticate
@company_autentication
def pix_revision(request):
    txid = request.POST.get('txid', None)

    headers = _headers()
    certificado = f'{settings.PATH_CREDENTIALS}{settings.CERT_DEV}'

    if txid:
        url = f'{settings.GN_BASE_URL}/v2/cob/{txid}'
    else:
        return JsonResponse({'message': 'Informe o localizador da cobrança', 'status': 404})

    payload = json.dumps({
            "calendario": {
                "expiracao": 600
            },
            "devedor": {
                "nome": "Fukuma",
                "cpf": "70921227086"
            },
            "valor": {
                "original": "3000.00"
            },
            "chave": "03659197050",
            "solicitacaoPagador": "Informe o número ou identificador do pedido.",
            "infoAdicionais": [
                {
                "nome": "Campo 1",
                "valor": "valor 1"
                }
            ]
            })
    print(generate_key_pix())

    response = requests.request("PATCH", url, headers=headers, data=payload, cert=certificado)

    return JsonResponse({
        'response': response.json(),
        'status': 200
    })
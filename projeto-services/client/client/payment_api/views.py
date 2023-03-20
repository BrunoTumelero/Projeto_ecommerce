from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

import requests
import base64
import json
from gerencianet import Gerencianet

from client.public_api.decorators import user_authenticate, company_autentication
from .utils import _headers, txid_generator, generate_key_pix, validation_gn_keys, save_pix
from client.register.models import Shopping_Cart

@csrf_exempt
@user_authenticate
def pix_payment(request):
    value_purchases = Shopping_Cart.objects.filter(consumer=request.user.pk)
    total_item = [item.total for item in value_purchases]
    total_pushased = sum(total_item)
    name_infometion = request.POST.get('name_information', "Campo adicional")
    additional_information = request.POST.get('additional_inormation', "Informação adicional")

    print(value_purchases.product_id)
    company = value_purchases.product.company

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
        "nome": name_infometion,
        "valor": additional_information
        },
    ]
    })

    response = requests.request("POST", url, headers=headers, data=payload, cert=certificado)
    
    save_pix(response.json(), request.pk, company)

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

    response = requests.request("PATCH", url, headers=headers, data=payload, cert=certificado)

    return JsonResponse({
        'response': response.json(),
        'status': 200
    })

@csrf_exempt
@user_authenticate
@company_autentication
def pix_recived(request):
    start_date = request.POST.get('start_date', None) #timezone
    end_date = request.POST.get('end_date', None)
    txid = request.POST.get('txid', None)
    cpf = request.POST.get('cpf', None)
    cnpj = request.POST.get('cnpj', None)
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
    if txid:
        url += f'&txid={txid}'
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
def create_signature(request):
    plan_name = request.POST.get('plan_name', None)
    interval = request.POST.get('interval', None)
    repeat = request.POST.get('repeat', None)
 
    if interval:
        interval = int(interval)
    if repeat:
        repeat = int(repeat)

    gn = Gerencianet(validation_gn_keys())
    
    body = {
        'name': plan_name,
        'repeats': repeat,
        'interval': interval
    }
    
    plan =  gn.create_plan(body=body)

    return JsonResponse({
        **plan,
        'status': 200
    })

@csrf_exempt
@user_authenticate
def plan_subscribe(request):
    plan_id = request.POST.get('plan_id', None)
    consumer_id = request.POST.get('consumer_id', None)
    payment_type = request.POST.get('payment_type', None)
    
    gn = Gerencianet(validation_gn_keys())

    params = {
        'id': plan_id
    }

    body = {
        'items': [{
            'name': "Product 1",
            'value': 1000,
            'amount': 2
        }],
        'payment': {
            'credit_card': {
                'billing_address': {
                    'street': "Av. JK",
                    'number': 909,
                    'neighborhood': "Bauxita",
                    'zipcode': "35400000",
                    'city': "Ouro Preto",
                    'state': "MG"
                },
                'customer': {
                    'name': "Gorbadoc Oldbuck",
                    'cpf': "94271564656",
                    'email': "oldbuck@gerencianet.com.br",
                    'phone_number': "5144916523",
                    'birth': "1977-01-15",
                    'address': {
                        "street": "Nome da rua",
                        "number": 1234,
                        "neighborhood": "Nome do bairro",
                        "zipcode": "95123456",
                        "city": "Nome da cidade",
                        "complement": "789",
                        "state": "RS",},
                    "juridical_person": {
                        "corporate_name": "Company name",
                        "cnpj": "12345678996321",
                        },
                },
                "payment_token": "6426f3abd8688639c6772963669bbb8e0eb3c319",
                "discount": {
                    "type": "currency",
                        #"percentage": "",
                        #"currency": "100",
                    "value": 100,
                },
                "message": "",
                "trial_days": 7,
                
            }
        }
    }

    response = gn.one_step_subscription(params=params, body=body)

    return JsonResponse({
        **response,
    })
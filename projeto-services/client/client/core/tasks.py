from gerencianet import Gerencianet
from django.conf import settings
import requests
import base64

def generate_key_pix():
    credenciais = {
            'client_id': 'Client_Id_ec3f3b7a718656f4cafe2d66a65e096558520d27',
            'client_secret': 'Client_Secret_2f025a925ade7cf5bde4afc878fb692fd26134f8',
            'sandbox': True,
            'certificate': 'Projeto_dev\projeto-services\client\client\credinciais\dev.pem'
        }

    url = "https://api-pix-h.gerencianet.com.br/v2/gn/evp"

    payload={}
    headers = {
        'authorization': f'Bearer {get_token_api_payment()}',
        'x-client-cert-pem': 'Projeto_dev\projeto-services\client\client\credinciais\dev.pem'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

generate_key_pix()
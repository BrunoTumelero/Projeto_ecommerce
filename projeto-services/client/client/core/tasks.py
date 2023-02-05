
from django.conf import settings
import requests
import base64

client_id = 'Client_Id_ec3f3b7a718656f4cafe2d66a65e096558520d27'#settings.DEV_CLIENT_KEY,
client_secret = 'Client_Secret_2f025a925ade7cf5bde4afc878fb692fd26134f8' #settings.DEV_SECRET_KEY


certificado = 'client\credinciais\homologacao-436362-Verification-dev.pem'  # A variável certificado é o diretório em que seu certificado em formato .pem deve ser inserido

auth = base64.b64encode(
    (f"{client_id}:{client_secret}"
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

print(response.text)
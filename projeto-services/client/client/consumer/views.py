from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.conf import settings

from client.register.models import *
from .utils import _create_token
from client.consumer.forms import ConsumersCardsForm, WhishesForm, ProductsRatingForm
from client.public.decorators import user_authenticate

from cieloApi3 import *
import sys
import json

@csrf_exempt
def create_user(request):
    user_email = request.POST.get('user_email', None)
    password = request.POST.get('password', None)
    type_user = request.POST.get('type_user', None)
    full_name = request.POST.get('full_name', None)
    phone = request.POST.get('phone', None)
    cpf = request.POST.get('cpf', None)

    if full_name and user_email and password:
        #Check email already exists
        if User.objects.filter(email=user_email).exists():
            try:
                user = User.objects.get(email=user_email)
            except User.MultipleObjectsReturned:
                return JsonResponse({'message': 'Email já cadastrado', 'status': 400})
            if not user.is_company:
                return JsonResponse({'message': 'Email já cadastrado', 'status': 400})
        else:
            #create user
            try:
                user = User.objects.create(email=user_email)
            except IntegrityError:
                #email duplicate
                return JsonResponse({'message': 'Emais já cadastrado', 'status': 400})

        if type_user == 'company':
            
            return JsonResponse({'message': 'Cadastro para usuários', 'status': 400})
        
        if type_user == 'consumer':
            user.email = user_email
            user.set_password(password)
            user.is_active = True
            user.is_consumer = True
            session_token = _create_token(user)
            user.save()
            consumer, _ = Consumers.objects.get_or_create(user=user)
            consumer.full_name = full_name
            consumer.whatsapp = phone
            consumer.cpf = cpf
            consumer.save()

            return JsonResponse({'message': 'Usuário cadastrado com sucesso', 'id': user.id, 'token': session_token, 'status': 200})

    return JsonResponse({'message': 'Erro ao cadastrar usuário', 'status': 200})

@csrf_exempt
@user_authenticate
def add_card(request):
    data = request.POST.copy()

    form = ConsumersCardsForm(data=data)

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Cartão adicionado com sucesso', 'status': 200})
    else:
        print(form.errors)
        return JsonResponse({'message': 'Erro ao salvar cartão', 'status': 400})

@csrf_exempt
@user_authenticate
def get_consumer_product(request):
    product_id = request.POST.get('product_id', None)

    product = Products.objects.get(pk=product_id)

    return JsonResponse ({
        'product': product.to_product_json(),
        'status': 200
    })

@csrf_exempt
@user_authenticate
def search_product(request):
    text = request.POST.get('text', None)
    type_search = request.POST.get('type_search', None)

    skip = request.POST.get('skip', None)
    take = request.POST.get('take', None)

    if skip and take:
        try:
            skip = int(skip)
            take = int(take) + skip
        except ValueError:
            return JsonResponse({'message': 'Erro de consulta', 'status': 400})
    else:
        skip = 0
        take = 999999999

    if type_search == 'basic':
        search = Products.objects.filter(product_name__icontains=text)
        product_card = [product.to_product_json() for product in search]

    return JsonResponse({
        'product_list': product_card,
        'status': 200
    })

@csrf_exempt
@user_authenticate
def add_whishes_list(request, pk=None):
    data = request.POST.copy()

    if pk:
        list_whishes = Whishes.objects.get(pk=pk)
        form = WhishesForm(instance=list_whishes, data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': f'Itens adicionados com sucesso na lista: {list_whishes.name_whishes_list}', 'status': 200})
        else:
            return JsonResponse({'message': f'Erro ao adicionar itens na lista: {list_whishes.name_whishes_list}', 'status': 400})
    else:
        form = WhishesForm(data=data)
        name_list = data['name_whishes_list']

        if form.is_valid():
            form.save()
            return JsonResponse({'message': f'Lista: {name_list} criada com sucesso', 'status': 200})
        else:
            return JsonResponse({'message': f'Erro ao criar lista: {name_list}', 'status': 400})

@csrf_exempt
@user_authenticate
def rating_product(request):
    user = request.POST.get('user', None)
    rated_product = request.POST.get('product', None)
    data = request.POST.copy()

    if user and rated_product:
        try:
            rating = ProductsRating.objects.filter(user=user, product=rated_product).first()
            form = ProductsRatingForm(instance=rating, data=data)
        except ProductsRating.DoesNotExist:
            form = ProductsRatingForm(data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Produto avaliado.', 'status': 200})
        else:
            print(form.errors)
            return JsonResponse({'message': 'Erro ao avaliar.', 'status': 400})
    
    return JsonResponse({'message': 'Erro.', 'status': 400})

@csrf_exempt
@user_authenticate
def card_payment(request):
    sys.path.insert(0, "./")
    # Configure o ambiente
    environment = Environment(sandbox=True)

    # Configure seu merchant, para gerar acesse: https://cadastrosandbox.cieloecommerce.cielo.com.br/
    merchant = Merchant(settings.MerchantId, settings.MerchantKey)

    # Crie uma instância de Sale informando o ID do pagamento
    sale = Sale('123')

    # Crie uma instância de Customer informando o nome do cliente
    sale.customer = Customer(request.user)

    # Crie uma instância de Credit Card utilizando os dados de teste
    # esses dados estão disponíveis no manual de integração
    credit_card = CreditCard('123', 'Visa')
    credit_card.expiration_date = '12/2018'
    credit_card.card_number = '0000000000000001'
    credit_card.holder = 'Fulano de Tal'

    # Crie uma instância de Payment informando o valor do pagamento
    sale.payment = Payment(15700)
    sale.payment.credit_card = credit_card

    # Cria instância do controlador do ecommerce
    cielo_ecommerce = CieloEcommerce(merchant, environment)

    # Criar a venda e imprime o retorno
    response_create_sale = cielo_ecommerce.create_sale(sale)
    print('----------------------response_create_sale----------------------')
    print(json.dumps(response_create_sale, indent=2))
    print('----------------------response_create_sale----------------------')

    # Com a venda criada na Cielo, já temos o ID do pagamento, TID e demais
    # dados retornados pela Cielo
    payment_id = sale.payment.payment_id

    # Com o ID do pagamento, podemos fazer sua captura,
    # se ela não tiver sido capturada ainda
    response_capture_sale = cielo_ecommerce.capture_sale(payment_id, 15700, 0)
    print('----------------------response_capture_sale----------------------')
    print(json.dumps(response_capture_sale, indent=2))
    print('----------------------response_capture_sale----------------------')

    # E também podemos fazer seu cancelamento, se for o caso
    response_cancel_sale = cielo_ecommerce.cancel_sale(payment_id, 15700)
    print('---------------------response_cancel_sale---------------------')
    print(json.dumps(response_cancel_sale, indent=2))
    print('---------------------response_cancel_sale---------------------')

@csrf_exempt
@user_authenticate
def test(request):
    print('test')
    return JsonResponse({'message': 'teste realizado com sucesso'})
        
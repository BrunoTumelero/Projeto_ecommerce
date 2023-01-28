from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from django.conf import settings

from client.register.models import *
from .utils import _create_token
from client.consumer.forms import ConsumersCardsForm
from client.public.decorators import user_authenticate

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
def test(request):
    print('test')
    return JsonResponse({'message': 'teste realizado com sucesso'})
        
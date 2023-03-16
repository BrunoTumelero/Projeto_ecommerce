from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError

from client.register.models import *
from client.public_api.utils import _create_token
from client.consumer_api.utils import _create_activation_token
from client.company_api.forms import ProductsForm
from client.public_api.decorators import company_autentication, user_authenticate

@csrf_exempt
def create_company(request):
    email_owner = request.POST.get('email_owner', None)
    phone_owner = request.POST.get('phone_owner', None)
    cep = request.POST.get('cep', None)
    state = request.POST.get('state', None)
    city = request.POST.get('city', None)
    neighborhood = request.POST.get('neighborhood', None)
    street = request.POST.get('street', None)
    number = request.POST.get('number', None)
    complement = request.POST.get('complement', None)
    cpf_owner = request.POST.get('cpf_owner', None)
    cnpj = request.POST.get('cnpj', None)
    business_name = request.POST.get('business_name', None)
    public_name = request.POST.get('public_name', None)
    picture_url = request.POST.get('picture_url', None)
    business_phone = request.POST.get('business_phone', None)
    business_specialty = request.POST.get('business_specialty', None)
    plan = request.POST.get('plan', None)
    password = request.POST.get('password', None)

    if email_owner and password:
        if not User.objects.filter(email=email_owner).exists():
            user = User.objects.create_user(email=email_owner, password=password)
            user.is_active = True
            user.is_company = True
            session_token = _create_token(user)
            
            try:
                city = City.objects.get(name=city)
            except City.DoesNotExist:
                return JsonResponse({'message': 'Cidade não cadastrada', 'status': 400})
            try:
                state = State.objects.get(name=state)
            except State.DoesNotExist:
                return JsonResponse({'message': 'Cidade não cadastrada', 'status': 400})
            try:
                business_specialty = CompanySpecialty.objects.get(specialty=business_specialty)
            except CompanySpecialty.DoesNotExist:
                return JsonResponse({'message': 'Cidade não cadastrada', 'status': 400})
            try:
                company = Company(
                    user = user,
                    email_company = email_owner,
                    cep = cep,
                    state = state,
                    city = city,
                    neighborhood = neighborhood,
                    street = street,
                    number = number,
                    complement = complement,
                    cpf_owner = cpf_owner,
                    cnpj = cnpj,
                    business_name = business_name,
                    picture_url = picture_url,
                    public_name = public_name,
                    business_phone = business_phone,
                    business_specialty = business_specialty,
                    plan = plan,
                )

                company.save()
                user.save()

                #vincula a empresa ao usuário
                company.user.company = company
                company.save()
                return JsonResponse({'message':'Empresa cadastrada com sucesso.', '_id': user.id, 'status': 200, '_token': session_token})

            except User.MultipleObjectsReturned:
                return JsonResponse({'message': 'Email já cadastrado', 'status': 400})
        else:
            return JsonResponse({'message': 'Erro de formulário', 'status': 404})

    return JsonResponse({'message': 'Erro', 'status': 400})

@csrf_exempt
@user_authenticate
@company_autentication
def create_new_product(request):
    data = request.POST.copy()

    if data['product_name']:
        try:
            product = Products.objects.get(product_name=data['product_name'])
            form = ProductsForm(instance=product, data=data)
        except Products.DoesNotExist:
            form = ProductsForm(data=data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Produto adicionado com sucesso', 'status': 200})
        else:
            print(form.errors)
            return JsonResponse({'message': 'Erro ao salvar o produto', 'error': form.errors, 'status':404})
    
    return JsonResponse({'message': 'Erro ao adicionar o produto', 'status': 400})

@csrf_exempt
@user_authenticate
@company_autentication
def edit_product(request, pk):
    product_name = request.POST.get('product_name', None)
    product_description = request.POST.get('product_description', None)
    product_category = request.POST.get('product_category', None)
    product_price = request.POST.get('product_price', None)
    is_avaliable = request.POST.get('is_avaliable', None)
    
    if pk:
        if product_category:
            category = ProductCategory.objects.get(pk=product_category)
        product = Products.objects.get(pk=pk)
        product.company = request.user.company
        product.product_name = product_name
        product.product_description = product_description
        product.product_category = category
        product.product_price = product_price
        product.is_avalable = is_avaliable if is_avaliable else False
        
        product.save()
        
        return JsonResponse({'message': 'Produto alterado com sucesso', 'status': 200})
        
    return JsonResponse({'message': 'Produto inválido', 'status': 400})

@csrf_exempt
@user_authenticate
@company_autentication
def create_employee(request):
    full_name = request.POST.get('full_name', None)
    user_email = request.POST.get('user_email', None)
    password = request.POST.get('password', None)
    phone = request.POST.get('phone', None)
    cpf = request.POST.get('cpf', None)
    
    if full_name and user_email and password and phone and cpf:
        print(11111)
        try:
            user = User.objects.get(email=user_email)
            user.company_id = request.user.pk
            session_token = _create_token(user)
            user.save()
            return JsonResponse({'message': 'Usuário cadastrado com sucesso', 'id': user.id, 'token': session_token, 'status': 200})
        except User.DoesNotExist:
            try:
                user.email = user_email
                user.set_password(password)
                user.is_active = True
                user.is_consumer = True
                user.is_company = True
                user.activation_key = _create_activation_token()
                session_token = _create_token(user)
                user.save()
                consumer, _ = Consumers.objects.get_or_create(user=user)
                consumer.full_name = full_name
                consumer.whatsapp = phone
                consumer.cpf = cpf
                consumer.save()
            
                return JsonResponse({'message': 'Usuário cadastrado com sucesso', 'id': user.id, 'token': session_token, 'status': 200})
            except IntegrityError:
                #email duplicate
                return JsonResponse({'message': 'Emais já cadastrado', 'status': 404})
    return JsonResponse({'message': 'Informe os campos obrigatórios', 'status': 400})
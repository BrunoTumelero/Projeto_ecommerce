from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError

from client.register.models import *
from client.public.utils import _create_token
from client.company.forms import ProductsForm
from client.public.decorators import company_autentication, user_authenticate

@csrf_exempt
def create_company(request):
    name_owner = request.POST.get('name_owner', None)
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
                    name_owner = name_owner,
                    email_owner = email_owner,
                    phone_owner = phone_owner,
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
            #create user
            try:
                user = User.objects.create(email=email_owner)
            except IntegrityError:
                #email duplicate
                return JsonResponse({'message': 'Emais já cadastrado', 'status': 400})

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
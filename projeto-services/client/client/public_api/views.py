from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .utils import _create_token
from .decorators import user_authenticate
from client.register.models import UserSession, Log, User, Permission, Products, ProductCategory, Consumers

@csrf_exempt
def login(request):
    user_email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    type_user = request.POST.get('type', None)

    if user_email and password:
        user = authenticate(username=user_email, password=password, email=user_email)
        if user is not None:
            
            if user.is_consumer and user.is_company:
                _type = 'consumer_company'
            elif user.is_consumer and not user.is_company:
                _type = 'consumer'
            elif user.is_company and not user.is_consumer:
                _type = 'company'
            elif user.is_staff:
                _type = 'staff'

            if _type == type_user:
                session_token = _create_token(user)

                #consumer =  Consumers.objects.get(user_id=user.id)

                return JsonResponse({
                    '_id': user.id,
                    '_token': session_token,
                    'type': _type,
                    #'full_name': consumer.full_name,
                    #'picture_url': consumer.picture_url,
                    'message': 'Login efetuado com sucesso.',
                    'status': 200
                })
            else: 
                return JsonResponse({'message':'Usuário ou senha inválidos.', 'status': 400})

        else:
            return JsonResponse({'message':'Usuário ou senha inválidos.', 'status': 400})
    else:
        return JsonResponse({'message':'Usuário ou senha inválidos.', 'status': 400})

@csrf_exempt
@user_authenticate
def logout(request):
    _token = request.POST.get('_token', None)

    if _token:
        user = authenticate(session_token=_token)

        if user is not None:
            UserSession.objects.filter(user=user, session_token=_token).delete()
            return JsonResponse({'message': 'Sessão finalizada com sucesso', 'status': 200})
    
    return JsonResponse({'message': 'Algo deu errado', 'status': 400})

@csrf_exempt
@user_authenticate
def log_session(request):
    session_type = request.POST.get('type', None)
    url = request.POST.get('url', '/')

    if session_type:
        if ((request.user.is_consumer and session_type == 'consumer') or
        (request.user.is_company and session_type == 'company') or
        (request.user.is_staff and session_type == 'staff') or
        (request.user.is_consumer and request.user.is_company and session_type == 'consumer_company')):

            permissions = [perm.permission_name for perm in Permission.objects.all()]

            #Save url address on log
            try:
                log = Log(user=request.user, url=url, authorized=True)
                log.save()
            except Exception:
                pass
        
        return JsonResponse({
            'activated': request.user.is_activated,
            'permissions': permissions,
            'status': 200
        })

@csrf_exempt
def get_products(request):
    products = [product.to_product_json() for product in Products.objects.all()]

    return JsonResponse({'Products': products, 'status': 200})

@csrf_exempt
def get_products_category(request):
    products = [product.to_json() for product in ProductCategory.objects.all()]

    return JsonResponse({'Products': products, 'status': 200})
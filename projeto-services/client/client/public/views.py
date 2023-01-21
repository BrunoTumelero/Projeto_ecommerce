from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse

from .utils import _create_token
from .forms import StateForm, CityForm
from client.register.models import State, City
from client.public.decorators import staff_autentication

@csrf_exempt
def login(request):
    user_email = request.POST.get('email', None)
    password = request.POST.get('password', None)

    if user_email and password:
        user = authenticate(username=user_email, password=password, email=user_email)
        if user is not None:
            session_token = _create_token(user)
            if user.is_consumer and user.is_company:
                _type = 'consumer_company'
            elif user.is_consumer and not user.is_company:
                _type = 'consumer'
            elif user.is_company and not user.is_consumer:
                _type = 'company'
            #elif user.is_staff:
                #_type = 'staff'

            return JsonResponse({
                '_id': user.id,
                '_token': session_token,
                'type': '_type',
                'message': 'Login efetuado com sucesso.',
                'status': 200
            })
        else:
            return JsonResponse({'message':'Usuário ou senha inválido.', 'status': 400})
    else:
        return JsonResponse({'message':'Usuário ou senha inválido.', 'status': 400})

@csrf_exempt
@staff_autentication
def create_state(request):
    data = request.POST.copy()

    try:
        state = State.objects.get(uf=data['uf'])
        form = StateForm(instance=state, data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Estado salvo com sucesso', 'status': 200})
        print(form.errors)
    except State.DoesNotExist:
        form = StateForm(data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Estado salvo com sucesso', 'status': 200})
        print(form.errors)

    return JsonResponse({'message': 'Estado inválido', 'status': 400})

@csrf_exempt
@staff_autentication
def create_city(request):
    data = request.POST.copy()

    try:
        city = City.objects.get(name=data['name'])
        form = CityForm(instance=city, data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Estado salvo com sucesso', 'status': 200})
        print(form.errors)
    except City.DoesNotExist:
        form = CityForm(data=data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cidade salva com sucesso', 'status': 200})
        print(form.errors)

    return JsonResponse({'message': 'Cidade inválida', 'status': 400})
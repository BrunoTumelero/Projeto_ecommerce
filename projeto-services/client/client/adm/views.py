from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .decorators import staff_authenticate
from client.register.models import State, City
from .forms import StateForm, CityForm
from client.register.models import User

@csrf_exempt
@staff_authenticate
def user_permission(request):
    data = request.POST.copy()

    if data['email']:
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return JsonResponse({'message': 'Usuário inválido', 'status': 400})
        if data['is_staff']:
            user.is_staff = True
            user.save()
            return JsonResponse({'message': 'Status staff alterado com sucesso', 'status': 200})
        if data['is_superuser']:
            user.is_superuser = True
            user.save()
            return JsonResponse({'message': 'Status superuser alterado com sucesso', 'status': 200})
    return JsonResponse({'message': 'Informe o email do usuário', 'status': 400})

@csrf_exempt
@staff_authenticate
def remove_permisson(request):
    data = request.POST.copy()

    if data['email']:
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return JsonResponse({'message': 'Usuário inválido', 'status': 400})
        if user.is_staff and data['is_staff']:
            user.is_staff = False
            user.save()
            return JsonResponse({'message': 'Status staff alterado com sucesso', 'status': 200})
        if user.is_superuser and data['is_superuser']:
            user.is_superuser = False
            user.save()
            return JsonResponse({'message': 'Status staff alterado com sucesso', 'status': 200})
    return JsonResponse({'message': 'Informe o email do usuário', 'status': 400})

@csrf_exempt
@staff_authenticate
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
@staff_authenticate
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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .decorators import staff_authenticate
from client.register.models import State, City, ProductCategory, User, CompanySpecialty, SubCategory, Permission, CompanyPermission
from .forms import StateForm, CityForm, CompanySpecialtyForm, ProductCategoryForm, ProductSubCategoryForm, PermissionForm, CompanyPermissionForm

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

@csrf_exempt
@staff_authenticate
def delete_account(request):
    user_id = request.POST.get('user_id')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Usuário inválido', 'status': 400})

    #delete permissions
    user.permisions.all().delete() #related_name

    #delete user
    user.delete()

    return JsonResponse({'message': 'Usuário deletado com sucesso', 'status': 200})

@csrf_exempt
@staff_authenticate
def create_specialty(request):
    data = request.POST.copy()

    if data['specialty']:
        try:
            type_specialty = CompanySpecialty.objects.get(specialty=data['specialty'])
            form = CompanySpecialtyForm(instance=type_specialty, data=data)

            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Especialidade salva com sucesso', 'status': 200})
        except CompanySpecialty.DoesNotExist:
            form = CompanySpecialtyForm(data=data)

            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Especialidade salva com sucesso', 'status': 200})
    return JsonResponse({'message': 'Erro ao salvar especialidade', 'status': 400})

@csrf_exempt
@staff_authenticate
def create_sub_category(request):
    data = request.POST.copy()

    if data['sub_category']:
        try:
            sub_category = SubCategory.objects.get(sub_category=data['sub_category'])
            form = ProductSubCategoryForm(instance=sub_category, data=data)
        except SubCategory.DoesNotExist:
            form = ProductSubCategoryForm(data=data)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Sub categoria salva com sucesso', 'status': 200})
        else:
            print(form.errors)
    return JsonResponse({'message': 'Erro ao salvar sub categoria', 'error': form.errors, 'status': 404})

@csrf_exempt
@staff_authenticate
def create_product_category(request):
    data = request.POST.copy()

    if data['category']:
        try:
            cat = ProductCategory.objects.get(category=data['category'])
            form = ProductCategoryForm(instance=cat, data=data)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Categoria adicionada comsucesso', 'status': 200})
        except ProductCategory.DoesNotExist:
            form = ProductCategoryForm(data=data)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Categoria adicionada comsucesso', 'status': 200})
            else:
                print(form.errors)
                return JsonResponse({'message': 'Erro', 'status': 400})
    return JsonResponse({'message': 'Informe a categoria', 'status': 400})

@csrf_exempt
@staff_authenticate
def create_permission(request):
    permission_name = request.POST.get('permission', None)
    data = request.POST.copy()
    
    if permission_name:
        data['permission_name'] = permission_name.lower()
        try:
            permission = Permission.objects.get(permission_name=data['permission_name'])
            form = PermissionForm(instance=permission, data=data)
        except Permission.DoesNotExist:
            form = PermissionForm(data=data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Permissão criada com sucesso', 'status': 200})
        else:
            print(form.errors)
            return JsonResponse({'message': 'Erro', 'status': 400})
    return JsonResponse({'message': 'Informe campos obrigatórios', 'status': 404})

@csrf_exempt
@staff_authenticate
def create_company_permissions(request):
    data = request.POST.copy()
    
    try:
        permission = CompanyPermission.objects.get(company=data['company'])
        form = CompanyPermissionForm(instance=permission, data=data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Permissões alteradas com sucesso', 'status': 200})
    except CompanyPermission.DoesNotExist:
        form = CompanyPermissionForm(data=data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Permissões alteradas com sucesso', 'status': 200})
        
    return JsonResponse({'message': 'ERRO', 'status': 400})
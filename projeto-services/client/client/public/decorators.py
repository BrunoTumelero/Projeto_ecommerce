from django.contrib.auth import authenticate
from django.http import JsonResponse

def user_authenticate(function):

    def wrap(request, *args, **kwargs):
        user = authenticate(session_token=request.POST.get('_token', None))

        if user is None:
            return JsonResponse({'message': 'Você precisa estar autenticado.', 'status': 400})

        request.user = user

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
    
def company_autentication(function):

    def find_token(request, *args, **kwargs):
        if hasattr(request, 'user') and not request.user.is_company:
            return JsonResponse({'menssage': 'Empresa autorizado', 'status': 403})

        return function(request, *args, **kwargs)

    find_token.__doc__ = function.__doc__
    find_token.__name__ = function.__name__

    return find_token

def staff_autentication(codename):

    def method_token(function):

        def find_token(reuquest, *args, **kwargs):
            _function = function(reuquest, *args, **kwargs)

            if reuquest.user.is_staff or reuquest.user.is_superuser:
                return _function

            if not reuquest.user.permissions.filter(permission__codename=codename).exists():
                return JsonResponse({'message': 'Você não tem permissão', 'status':403})

            return _function

        return find_token

    return method_token
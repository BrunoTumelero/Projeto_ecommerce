from django.contrib.auth import authenticate
from django.http import JsonResponse

def staff_authenticate(function):
    """
        Validation of staff_user
        """
    def warp(request, *args, **kwargs):
        user = authenticate(session_token=request.POST.get('_stafftoken', None))
        if user is None:
            return JsonResponse({'message': 'Acesso não permitido', 'status': 400})

        request.user = user

        return function(request, *args, **kwargs)

    warp.__doc__ = function.__doc__
    warp.__name__ = function.__name__

    return warp
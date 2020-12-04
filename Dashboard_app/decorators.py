from django.http import HttpResponse
from django.shortcuts import redirect, render


def view_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff and request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(f"Sorry '{request.user}'........!!!! you are not authorised to view this page !")

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'dashboard_app/not_authorised.html')

        return wrapper_func

    return decorators

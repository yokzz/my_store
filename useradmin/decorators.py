from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            raise Http404()
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
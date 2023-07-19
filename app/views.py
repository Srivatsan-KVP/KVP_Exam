from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.models import User

from utils import parseForm
from . import forms


# Create your views here.
def login(req):
    if req.method == 'POST':
        valid, data = parseForm(forms.LoginForm(req.POST))

        if not valid: return JsonResponse(data)
        user = authenticate(username=data['username'], password=data['password'])

        cond = False
        if data['isadmin']: cond = (not User.objects.get(pk=user.pk).is_superuser)
        if user is None or cond: return JsonResponse({ 'valid': False, 'message': 'Invalid credentials!' })

        dj_login(req, user)
        return JsonResponse({ 'valid': True, 'url': 'admin/' if data['isadmin'] else '/' })
    
    if req.user.is_authenticated:
        return redirect('/admin/') if User.objects.get(pk=req.user.pk).is_superuser else redirect('/')
        
    return render(req, 'app/login.html')

def logout(req):
    dj_logout(req)
    return redirect('/login/')
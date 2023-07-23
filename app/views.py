from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from utils import parseForm, shouldAllow, getData
from . import forms, models, logic
from datetime import datetime


def __parseDate(date: str):
    spl = [int(i) for i in date.split('-')]
    return datetime(spl[2], spl[1], spl[0]).date()


# Create your views here.
def login(req):
    if req.method == 'POST':
        valid, data = parseForm(forms.LoginForm(req.POST))

        if not valid: return JsonResponse(data)
        user = authenticate(username=data['username'], password=data['password'])

        if user is None or data['isadmin'] != User.objects.get(pk=user.pk).is_superuser: 
            return JsonResponse({ 'valid': False, 'message': 'Invalid credentials!' })

        dj_login(req, user)
        return JsonResponse({ 'valid': True, 'url': 'admin/' if data['isadmin'] else '/' })
    
    if req.user.is_authenticated:
        return redirect('/admin/') if User.objects.get(pk=req.user.pk).is_superuser else redirect('/')
        
    return render(req, 'app/login.html')


def logout(req):
    if req.user.is_authenticated:
        dj_logout(req)
    return redirect('/login/')


def saved(req, date):
    data = getData()
    return render(req, 'app/saved.html', {
        'info': data.get(''.join(date.split('-')), {}),
        'date': date
    })



# TEACHERS
@login_required(login_url='/login/')
def main(req):
    if not shouldAllow(req, False): return redirect('/admin/')
    
    if req.method == 'POST':
        valid, data = parseForm(forms.EntryForm(req.POST))
        if not valid: return JsonResponse(data)

        return JsonResponse(logic.addEntry(data, __parseDate(req.POST['date'])))
    
    if not req.GET.get('date', False):
        return render(req, 'app/main.html')
    
    ctx = {
        'info': {}, 'rooms': models.Room.objects.all(),
        'entries': models.Entry.objects.filter(date=__parseDate(req.GET['date']))
    }
    
    for link in models.Link.objects.filter(teacher=models.Teacher.objects.get(user=req.user)):
        ctx['info'][link.room] = models.Entry.objects.filter(room=link.room)
    
    return render(req, 'app/main.html', ctx)





# ADMIN
@login_required(login_url='/login/')
def admin(req):
    if not shouldAllow(req, True): return redirect('/')

    if req.method == 'POST':
        valid, data = parseForm(forms.AdminForm(req.POST))
        if not valid: return JsonResponse(data)

        if data['add']:
            if data['add'] == 'subject':
                return JsonResponse(logic.addSubject(data['uid'], req.POST['name']))
            
            if data['add'] == 'class':
                return JsonResponse(logic.addClass(data['uid'], req.POST['name'], req.POST['strength'], req.POST['group']))
            
            if data['add'] == 'teacher':
                return JsonResponse(logic.addTeacher(req.POST))
            
            if data['add'] == 'link':
                return JsonResponse(logic.addLink(data['uid'], req.POST))
            
            if data['add'] == 'exam':
                return JsonResponse(logic.addExam(req.POST))

        else:
            if data['remove'] == 'subject':
                models.Subject.objects.filter(uid=data['uid']).delete()
                return JsonResponse({ 'valid': True })
            
            if data['remove'] == 'class':
                models.Room.objects.filter(uid=data['uid']).delete()
                return JsonResponse({ 'valid': True })
            
            if data['remove'] == 'link':
                models.Link.objects.filter(uid=data['uid']).delete()
                return JsonResponse({ 'valid': True })
            
            return JsonResponse({ 'valid': False, 'message': 'Invalid submission!' })

    rel: dict[models.Room, list[models.Link]] = {}
    for room in models.Room.objects.all():
        rel[room] = [i for i in models.Link.objects.filter(room=room)]

    ctx = {
        'subjects': models.Subject.objects.all(),
        'rooms': models.Room.objects.all(),
        'teachers': models.Teacher.objects.all(),
        'relations': rel,
        'dates': [i[:2] + '-' + i[2:4] + '-' + i[4:] for i in getData().keys()]
    }

    return render(req, 'app/admin.html', ctx)




# COMMON
@login_required(login_url='/login/')
def profile(req):

    if req.method == 'POST':
        if req.POST.get('name', False):
            models.Teacher.objects.filter(user=req.user).update(name=req.POST['name'])
            return JsonResponse({ 'valid': True, 'message': 'Updated!' })
        
        elif req.POST.get('username', False):
            User.objects.filter(username=req.user.username).update(username=req.POST['username'])
            return JsonResponse({ 'valid': True, 'message': 'Updated!' })

        elif req.POST.get('password', False):
            if req.POST['password'] != req.POST['confirm']:
                return JsonResponse({ 'valid': False, 'message': 'Passwords do not match' })
            req.user.set_password(req.POST['password'])
            req.user.save()
            return JsonResponse({ 'valid': True, 'message': 'Updated!' })

        elif req.POST.get('delete', False):
            User.objects.filter(username=req.user.username).delete()
            return JsonResponse({ 'valid': True, 'url': '/logout/' })

        return JsonResponse({ 'valid': False, 'message': 'Invalid Submission!' })

    ctx = {}
    if not User.objects.get(pk=req.user.pk).is_superuser:
        ctx['name'] = models.Teacher.objects.get(user=req.user).name

    return render(req, 'app/profile.html', ctx)
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profil
from . forms import LoginForm, ApiForm
from . serviceuser import (
    connect
)
from . import serviceentity as sentity
from . import servicebranch as sbranch
from . import serviceservice as sservice
from . import servicefunction as sfunction
from . import servicecategorie as scategorie
from . import servicearticle as sarticle
from . import servicestockageaera as sstockageaera
from . import servicecareer as scareer
from . import servicevillage as svillage
from . import servicestockageaeralv as sstockageaeralv
from . import servicecareerlv as scareerlv
from . import servicecareerarticle as scareerarticle

from . constances import (
    ENDPOINT_ENTITY,
    ENDPOINT_CAREER,
    ENDPOINT_USER
)

import http.client
import json


# Create your views here.
def index(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect(reverse('frontend_dashboard'))
    return render(request, 'frontend/login.html')


def f_login(request):
    if request.method == 'GET':
        return redirect(reverse('frontend_index'))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
 
            #user = authenticate(
            #    request,
            #    username=email,
            #    password=password
            #)
            #login(request, user)
            #return redirect(reverse('frontend_dashboard'))
            
            res = connect(email=email, password=password)
            if res.get('detail', 0) != 0:
                messages.error(request, res['detail'])
                return render(
                    request,
                    'frontend/login.html',
                    {'form': form}
                )
            else:
                request.infoUser = res
                try:
                    user = User.objects.get(username=email)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=email,
                        password=password
                    )
                    profil = Profil()
                    profil.access = "e"
                    profil.refresh = "e"
                    profil.user = user
                    profil.save()

                user.profil.access = res["access"]
                user.profil.refresh = res['refresh']
                user.profil.save()

                if user.is_active:
                    user = authenticate(
                        request,
                        username=email,
                        password=password
                    )
                    login(request, user)
                    return redirect(reverse('frontend_dashboard'))
                else:
                    messages.warning(request, 'Compte suspendu')
                    return render(
                        request,
                        'frontend/login.html',
                        {'form': form}
                    )
        else:
            messages.error(
                request,
                "Veuillez compléter le formulaire ci-dessus"
            )
            return render(
                request,
                'frontend/login.html',
                {'form': form}
            )


@login_required(login_url='/')
def dashbord(request):
    #logout(request)
    #request.user.profil.access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwMTU1Nzg0LCJpYXQiOjE3MDAwNjkzODQsImp0aSI6IjI1ZjJjNGRmNDFkNjRjN2U4MGFlMDgyYjY0YjcyMjNiIiwidXNlcl9pZCI6IjRmNjk2ZTkyLTVkNGUtNGQ0MS04MTIzLTJhMjFjNWYzNDg1MyJ9.7ebkID1iFbG73FYMiGCoYKExVSCyqLbz67GeNb4zl20"
    #request.user.profil.save()
    return render(request, 'frontend/index.html')


@login_required(login_url='/')
def user(request):
    data = {}
    data['access'] = request.user.profil.access
    data['refresh'] = request.user.profil.refresh
    return JsonResponse(data, status=200)


@login_required(login_url='/')
def entity(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sentity.read(request=request)
    elif request.method == "POST":
        data = sentity.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def branch(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sbranch.read(request=request)
    elif request.method == "POST":
        data = sbranch.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def service(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sservice.read(request=request)
    elif request.method == "POST":
        data = sservice.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def function(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sfunction.read(request=request)
    elif request.method == "POST":
        data = sfunction.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def categorie(request):
    data = {"status": 400}
    if request.method == "GET":
        data = scategorie.read(request=request)
    elif request.method == "POST":
        data = scategorie.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def article(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sarticle.read(request=request)
    elif request.method == "POST":
        data = sarticle.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def stockageaera(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sstockageaera.read(request=request)
    elif request.method == "POST":
        data = sstockageaera.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def career(request):
    data = {"status": 400}
    if request.method == "GET":
        data = scareer.read(request=request)
    elif request.method == "POST":
        data = scareer.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def stockageaeralv(request):
    data = {"status": 400}
    if request.method == "GET":
        data = sstockageaeralv.read(request=request)
    elif request.method == "POST":
        data = sstockageaeralv.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def careerlv(request):
    data = {"status": 400}
    if request.method == "GET":
        data = scareerlv.read(request=request)
    elif request.method == "POST":
        data = scareerlv.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def careerarticle(request):
    data = {"status": 400}
    if request.method == "GET":
        data = scareerarticle.read(request=request)
    elif request.method == "POST":
        data = scareerarticle.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def village(request):
    data = {"status": 400}
    if request.method == "GET":
        data = svillage.read(request=request)
    elif request.method == "POST":
        data = svillage.create(request=request)
    return JsonResponse(data, status=data['status'])


@login_required(login_url='/')
def api(request):
    data = {"status": 400}

    if request.method == "GET":
        form = ApiForm(request.GET)
        payload = ''
        verb = 'GET'
    elif request.method == "POST":
        charge = json.loads(request.body)
        form = ApiForm(charge)
        payload = json.dumps(charge)
        verb = 'POST'

    if form.is_valid():
        end = form.cleaned_data['end']
        detail = form.cleaned_data['detail']
        terminaison = form.cleaned_data['terminaison']
        id = form.cleaned_data.get('id', 'abc')
        action = form.cleaned_data.get('action', '')

        if end == 'career':
            ENDPOINT = ENDPOINT_CAREER
        elif end == 'entity':
            ENDPOINT = ENDPOINT_ENTITY
        else:
            ENDPOINT = ENDPOINT_USER

        conn = http.client.HTTPSConnection(ENDPOINT)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        if detail is True:
            conn.request(
                verb,
                "/" + str(terminaison) + "/" + str(id) + "/" + str(action),
                payload,
                headers
            )
        else:
            conn.request(verb, "/" + terminaison, payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['errors'] = {
           "end": form['end'].errors,
           "detail": form['detail'].errors,
           "terminaison": form['terminaison'].errors,
           "id": form['id'].errors,
           "action": form['action'].errors
        }
    return JsonResponse(data, status=data['status'])

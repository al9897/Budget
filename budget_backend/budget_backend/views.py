from django import http
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auth
from django.utils import timezone
import json
import pytz
import uuid

from datetime import datetime, timedelta

timezone = pytz.timezone('Europe/Amsterdam')


def index(request):
    return HttpResponse("WELCOME")


def register(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            user = User(
                full_name=body['full_name'],
                username=body['username'],
                password=body['password'],
                dob=body['dob'],
                email=body['email'],
                phone=body['phone'],
                adress=body['adress'],
                zipcode=body['zipcode'],
                country=body['country'],
                currency=body['currency'],
                iban=body['iban']
            )
            user.save()
            return HttpResponse("user is created, needs to login in ", status=200)

        except Exception as E:
            print(E)
            return HttpResponse("missing fields", status=422)
    else:
        return HttpResponse("method not allowed", status=405)


def loggedIn(request):
    if request.method == "GET":
        try:
            body = json.loads(request.body)
            _token = body['token']
            print(_token)
            auth = Auth.objects.get(token=_token)

            if auth is None:
                return HttpResponse("token doesn't exist", status=405)
            elif auth.expiry_date < datetime.now(timezone):
                return HttpResponse("Token expired", status=405)

            return HttpResponse("token valid", status=200)
        except Exception as E:
            print(E)
            return HttpResponse("Internal error", status=500)
    else:
        return HttpResponse("method not allowed, it needs to be 'GET'", status=405)


def login(request):
    if request.method in ['POST', 'GET']:
        try:
            body = json.loads(request.body)
            _username = body['username']
            _password = body['password']
            user = User.objects.get(username=_username, password=_password)
            if user is None:
                return HttpResponse('Unauthorized', status=401)
            else:
                _token = uuid.uuid4()
                auth = Auth(token=_token, user=user, expiry_date=datetime.now(timezone) + timedelta(hours=2))
                auth.save()

            print(auth.token)
            print(auth.user.id)
            print(auth.expiry_date)

            return JsonResponse({"token": _token, "user_id": user.id})
        except Exception as E:
            print(E)
            return HttpResponse("Wrong data", status=403)
    else:
        return HttpResponse("WRONG REQUEST, allowed GET OR POST", status=405)


def logout(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        _token = body['token']
        auth = Auth.objects.get(token=_token)
        if auth is not None:
            auth.delete()
            return HttpResponse("logout", status=200)
        return HttpResponse('Unauthorized, token not valid', status=401)
    else:
        return HttpResponse("WRONG HTTP REQUEST", status=405)

def profil(request, id):
    if request.method == 'GET':
        try:
            try:
                user = User.objects.get(id=id)
                dict_obj = model_to_dict(user)
                return JsonResponse(dict_obj)
            except ObjectDoesNotExist:
                return HttpResponse(" User not Not Found", status=404)
        except Exception as E:
            return HttpResponse(E, status=500)
    else:
        return HttpResponse("Wrong method, only GET allowed", status=405)

from . constances import ENDPOINT_ENTITY
from . forms import FunctionForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/function", payload, headers)
    response = conn.getresponse()
    data = {}
    if response.status == 429:
        data['status'] = response.status
        data['code'] = -1
    else:
        data = json.loads(response.read())
        data['status'] = response.status
        data['code'] = 0
    return data


def create(request):
    charge = json.loads(request.body)
    form = FunctionForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "name": form.cleaned_data['name'],
            "description": "non définie",
            "power": form.cleaned_data['power'],
            "service_id": form.cleaned_data['service_id']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/function", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "name": form['name'].errors,
            "description": form['description'].errors,
            "power": form['power'].errors,
            "service_id": form['service_id'].errors
        }
        data['status'] = 400
    return data

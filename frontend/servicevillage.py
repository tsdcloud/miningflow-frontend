from . constances import ENDPOINT_ENTITY
from . forms import ServiceForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/village", payload, headers)
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
    form = ServiceForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "name": form.cleaned_data['name'],
            "branch_id": form.cleaned_data['branch_id'],
        }
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/service", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "name": form['label'].errors,
            "branch_id": form['branch_id'].errors,
        }
        data['status'] = 400
    return data

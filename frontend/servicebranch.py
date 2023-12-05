from . constances import ENDPOINT_ENTITY
from . forms import BranchForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/branch", payload, headers)
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
    form = BranchForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "label": form.cleaned_data['label'],
            "firm_id": form.cleaned_data['firm_id'],
            "origin_id": form.cleaned_data['origin_id']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/branch", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "label": form['label'].errors,
            "firm_id": form['firm_id'].errors,
            "orgin_id": form['origin_id'].errors,
        }
        data['status'] = 400
    return data

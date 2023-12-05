from . constances import ENDPOINT_CAREER
from . forms import CareerForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/career", payload, headers)
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
    form = CareerForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "name": form.cleaned_data['name'],
            "village_id": form.cleaned_data['village_id'],
            "uin": form.cleaned_data['uin']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/career", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "name": form['name'].errors,
            "village_id": form['village_id'].errors,
            "uin": form['uin'].errors,
        }
        data['status'] = 400
    return data

from . constances import ENDPOINT_CAREER
from . forms import StockageAeraLvForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/stockageaeralv", payload, headers)
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
    form = StockageAeraLvForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "stockageaera_id": form.cleaned_data['stockageaera_id'],
            "last_demand_quantity": form.cleaned_data['last_demand_quantity'],
            "last_demand_volume": form.cleaned_data['last_demand_volume']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/stockageaeralv", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "stockageaera_id": form['stockageaera_id'].errors,
            "last_demand_quantity": form['last_demand_quantity'].errors,
            "last_demand_volume": form['last_demand_volume'].errors,
        }
        data['status'] = 400
    return data

from . constances import ENDPOINT_ENTITY
from . forms import EntityForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/firm", payload, headers)
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
    form = EntityForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "business_name": form.cleaned_data['business_name'],
            "acronym": form.cleaned_data['acronym'],
            "unique_identifier_number": form.cleaned_data[
                'unique_identifier_number'],
            "principal_activity": form.cleaned_data[
                'principal_activity'],
            "regime": form.cleaned_data['regime'],
            "tax_reporting_center": form.cleaned_data[
                'tax_reporting_center'],
            "trade_register": form.cleaned_data['trade_register'],
            "logo": form.cleaned_data['logo'],
            "type_person": form.cleaned_data['type_person']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_ENTITY)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/firm", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "business_name": form['business_name'].errors,
            "acronym": form['acronym'].errors,
            "unique_identifier_number": form[
                'unique_identifier_number'].errors,
            "principal_activity": form['principal_activity'].errors,
            "regime": form['regime'].errors,
            "tax_reporting_center": form['tax_reporting_center'].errors,
            "trade_register": form['trade_register'].errors,
            "logo": form['logo'].errors,
            "type_person": form['type_person'].errors,
        }
        data['status'] = 400
    return data

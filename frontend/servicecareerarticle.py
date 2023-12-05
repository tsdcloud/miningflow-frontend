from . constances import ENDPOINT_CAREER
from . forms import CareerArticleForm

import http.client
import json


def read(request):
    conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + request.user.profil.access
    }
    conn.request("GET", "/careerarticle", payload, headers)
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
    form = CareerArticleForm(charge)
    data = {}
    if form.is_valid():
        params = {
            "career_id": form.cleaned_data['career_id'],
            "stockage_id": form.cleaned_data['stockage_id'],
            "article_id": form.cleaned_data['article_id'],
            "price_sale": form.cleaned_data['price_sale'],
            "price_car": form.cleaned_data['price_car']
        }
        conn = http.client.HTTPSConnection(ENDPOINT_CAREER)
        payload = json.dumps(params)
        headers = {
            "Authorization": 'Bearer ' + request.user.profil.access,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/careerarticle", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        data['status'] = response.status
    else:
        data['descriptions'] = {
            "career_id": form['career_id'].errors,
            "stockage_id": form['stockage_id'].errors,
            "article_id": form['article_id'].errors,
            "price_sale": form['price_sale'].errors,
            "price_car": form['price_car'].errors,
        }
        data['status'] = 400
    return data

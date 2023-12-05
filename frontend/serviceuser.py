import http.client
import json
from . constances import ENDPOINT_USER


def connect(email: str, password: str):
    conn = http.client.HTTPSConnection(ENDPOINT_USER)
    payload = json.dumps({
        "username": email,
        "password": password
    })
    headers = {'Content-Type': 'application/json'}
    conn.request("POST", "/api/token/", payload, headers)
    res = conn.getresponse()
    e = res.read()
    try:
        data = json.loads(e.decode('utf8').replace("'", '"'))
    except:
        data = json.loads(e)
    return data


def getUser(authorization: str):
    conn = http.client.HTTPSConnection(ENDPOINT_USER)
    payload = ''
    headers = {
        "Authorization": 'Bearer ' + authorization
    }
    conn.request("GET", "/profil/myprofil/", payload, headers)
    response = conn.getresponse()
    data = json.loads(response.read())
    return data

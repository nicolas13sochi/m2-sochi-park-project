# 3rd patry requests
import requests
import json
from django.conf import settings
import base64

def test_api():
    url = f'https://randomuser.me/api/'

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {}

    params = {}
    
    response = requests.request("GET", url, headers=headers, data=payload, params=params)

    return response.json()


def post_lead(data):
    url = f"{settings.LEAD_API_URL}/api/v1/leads/create/"

    payload = json.dumps(data)
    headers = {
        'Api-Key': f'{settings.LEAD_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

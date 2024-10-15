import os
from dotenv import load_dotenv
import requests
import pytest

load_dotenv()

TOKEN = os.getenv('API_TOKEN')
BASE_URL = "https://gorest.co.in/public-api"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_create_user():
    payload = {
        "name": "zzz Johnson",
        "gender": "male",
        "email": "zzz.johnson@example.com",
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/users", json=payload, headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} insted"
    
    json_data = response.json()
    print(json_data)
    assert 'data' in json_data, "Response does not contain 'data' key"
    print('created user id: ',json_data['data']['id'])
    assert json_data['data']['name'] == "zzz Johnson", "User name does not match"
    assert json_data['data']['email'] == "zzz.johnson@example.com", "Email does not match"
    assert json_data['data']['gender'] == "male", "Gender does not match"
    assert json_data['data']['status'] == "active", "Status does not match"


def test_get_user_detail():
    user_id = 7472742
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_data = response.json()
    print(json_data)
    assert 'data' in json_data, "Response does not contain 'data' key"
    assert json_data['data']['name'] == "zzz Johnson", "User name does not match"
    assert json_data['data']['email'] == "zzz.johnson@example.com", "Email does not match"
    assert json_data['data']['gender'] == "male", "Gender does not match"
    assert json_data['data']['status'] == "active", "Status does not match"

def test_update_user_detail():
    user_id = 7472742
    payload = {
        "name": "zzz New Johnson",
    }
    response = requests.patch(f"{BASE_URL}/users/{user_id}", json=payload, headers=headers)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} insted"
    
    json_data = response.json()
    print(json_data)
    assert 'data' in json_data, "Response does not contain 'data' key"
    print('created user id: ',json_data['data']['id'])
    assert json_data['data']['name'] == payload['name'], "User name does not match"
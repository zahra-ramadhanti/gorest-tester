import requests
import pytest
from utils.random_generator import generate_random_email, generate_random_name, get_random_gender, get_random_status
from utils.logger_validator import log_and_assert, log_response_data, log_request_data
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('API_TOKEN')
BASE_URL = "https://gorest.co.in/public-api"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@pytest.fixture
def create_user():
    """Fixture to create a new user for positive test cases."""
    step_name = "Create User - Positive"
    name = generate_random_name()
    email = generate_random_email()
    gender = get_random_gender()
    status = get_random_status()
    
    request_data = {
        "name": name,
        "email": email,
        "gender": gender,
        "status": status
    }    

    log_request_data(request_data, step_name)
   
    response = requests.post(f"{BASE_URL}/users", json=request_data, headers=headers)
   
    log_response_data(response, step_name)
    
    return response

def test_create_user_positive(create_user):
    """Test case for creating a new user - positive case."""
    response = create_user
    response_json = response.json()

    expected_status_code = 200
    expected_values = {
        "code": 201,
        "meta": None,
        "data": {
            "id": response_json["data"]["id"],
            "name": response_json["data"]["name"],
            "email": response_json["data"]["email"],
            "gender": response_json["data"]["gender"],
            "status": response_json["data"]["status"],
        }
    }

    log_and_assert(response, expected_status_code, expected_values)

    data = response_json["data"]
    assert "id" in data, "Expected 'id' in response data."
    assert data["name"] is not None, "Expected 'name' to be present in response data."
    assert data["email"] is not None, "Expected 'email' to be present in response data."
    assert data["gender"] in ["male", "female"], "Expected 'gender' to be either 'male' or 'female'."
    assert data["status"] in ["active", "inactive"], "Expected 'status' to be either 'active' or 'inactive'."

def test_create_user_already_taken_email():
    step_name = "Create User - Already Taken Email"

    request_data = {
        "email": "7Z96utZH@example.com",
        "name": "7Z96utZH",
        "gender": "male",
        "status": "inactive",
    }

    log_request_data(request_data, step_name)
   
    response = requests.post(f"{BASE_URL}/users", json=request_data, headers=headers)
   
    log_response_data(response, step_name)

    expected_status_code = 200
    expected_values = {
        "code": 422,
        "meta": None,
        "data": [
            {
                "field": "email",
                "message": "has already been taken"
            }
        ] 
    }

    log_and_assert(response, expected_status_code, expected_values)


def test_get_user_details_positive(create_user):
    step_name = "Get User Details - Positive"
    user_detail = create_user.json()
    log_request_data({"user_id": user_detail['data']['id']}, step_name)

    response = requests.get(f"{BASE_URL}/users/{user_detail['data']['id']}", headers=headers)
   
    log_response_data(response, step_name)

    expected_status_code = 200
    expected_values = {
        "code": 200,
        "meta": None,
        "data": user_detail['data']
    }

    log_and_assert(response, expected_status_code, expected_values)
    
    data = response.json()["data"]
    assert data["name"] is not None, "Expected 'name' to be present in response data."
    assert data["email"] is not None, "Expected 'email' to be present in response data."
    assert data["gender"] in ["male", "female"], "Expected 'gender' to be either 'male' or 'female'."
    assert data["status"] in ["active", "inactive"], "Expected 'status' to be either 'active' or 'inactive'."


def test_get_user_details_non_existent():
    step_name = "Get User Detail - Non-existent User"
    non_existent_user_id = 999999  # Non-existent User ID
    response = requests.get(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
    response_json = response.json()

    expected_status_code = 200
    expected_values = {
        "code": 404,
        "meta": None,
        "data": {
            "message": "Resource not found"
        }
    }

    log_and_assert(response, expected_status_code, expected_values)

def test_update_user_already_taken_email(create_user):
    """Test case for updating user details with an already taken email"""
    step_name = "Update User Detail - Already Taken Email"
    user_id = create_user.json()["data"]["id"]
    update_field_invalid = {"email": "rAQUSqb5@example.com"} # Already Taken Email

    log_request_data(update_field_invalid, step_name)

    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_field_invalid, headers=headers)

    log_response_data(response, step_name)

    expected_status_code=200
    expected_values = {
        "code": 422,
        "meta": None,
        "data": [
            {
            "field": "email",
            "message": "has already been taken"
            }
        ]
    }

    log_and_assert(response, expected_status_code, expected_values)

def test_update_user_invalid_gender_and_status(create_user):
    step_name = "Update User - Invalid Gender and Status"
    user_id = create_user.json()["data"]["id"]
    update_fields_invalid = {
        "gender": "not_a_gender",
        "status": "not_a_status"
    }

    log_request_data(update_fields_invalid, step_name)
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_fields_invalid, headers=headers)
    
    log_response_data(response, step_name)

    expected_status_code = 200
    expected_values = {
        "code": 422,
        "meta": None,
        "data": [
            {
                "field": "gender",
                "message": "can't be blank, can be male of female"
            },
            {
                "field": "status",
                "message": "can't be blank"
            }
        ]
    }

    log_and_assert(response, expected_status_code, expected_values)


def test_delete_user_postive(create_user):
    step_name = "Delete User - Positive"
    user_id = create_user.json()["data"]["id"]

    log_request_data(user_id, step_name)

    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    response_json = response.json()

    log_response_data(response, step_name)
    
    expected_status_code=200
    expected_values = {
        "code": 204,
        "meta": None,
        "data": None
    }

    log_and_assert(response, expected_status_code, expected_values)


def test_delete_user_non_existent():
    """Test case for deleting a non-existent user."""
    step_name = "Delet User - Non-existent User"

    non_existent_user_id = 999999 # Non-exitend User ID

    log_request_data(non_existent_user_id, step_name)

    response = requests.delete(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
    response_json = response.json()

    log_response_data(response, step_name)
    
    expected_status_code=200
    expected_values = {
        "code": 404,
        "meta": None,
        "data": {
            "message": "Resource not found"
        }
    }

    log_and_assert(response, expected_status_code, expected_values)

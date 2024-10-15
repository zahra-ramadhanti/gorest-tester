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

    log_request_data(request_data, step_name="Create User Request Body")
   
    response = requests.post(f"{BASE_URL}/users", json=request_data, headers=headers)
   
    log_response_data(response, step_name="Create User Response")
    
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

    print(response_json)


    log_and_assert(response, expected_status_code, expected_values)

    # Additional assertions for specific fields
    data = response_json["data"]
    assert "id" in data, "Expected 'id' in response data."
    assert data["name"] is not None, "Expected 'name' to be present in response data."
    assert data["email"] is not None, "Expected 'email' to be present in response data."
    assert data["gender"] in ["male", "female"], "Expected 'gender' to be either 'male' or 'female'."
    assert data["status"] in ["active", "inactive"], "Expected 'status' to be either 'active' or 'inactive'."

def test_get_user_details(create_user):
    """Test case for getting user details."""
    user_detail = create_user.json()
    log_request_data({"user_id": user_detail['data']['id']}, step_name="Get User Details")

    response = requests.get(f"{BASE_URL}/users/{user_detail['data']['id']}", headers=headers)
   
    log_response_data(response, step_name="Get User Details")

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
    """Test case for getting details of a non-existent user."""
    non_existent_user_id = 999999  # Assuming this user ID does not exist
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

def test_update_user_invalid_gender(create_user):
    """Test case for updating user details with an invalid gender."""
    user_id = create_user.json()["data"]["id"]
    update_fields_invalid = {"gender": "not_a_gender"}

    log_request_data(update_fields_invalid, step_name="Update with Invalid Gender Input")
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_fields_invalid, headers=headers)
    
    log_response_data(response, step_name="Update with Invalid Gender Input")

    expected_status_code=200
    expected_values = {
        "code": 422,
        "meta": None,
        "data": [
            {
            "field": "gender",
            "message": "can't be blank, can be male of female"
            }
        ]
    }

    log_and_assert(response, expected_status_code, expected_values)

def test_delete_user(create_user):
    """Test case for deleting a user."""
    user_id = create_user.json()["data"]["id"]

    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    response_json = response.json()

    log_response_data(response, step_name="Delete A Valid User")
    
    expected_status_code=200
    expected_values = {
        "code": 204,
        "meta": None,
        "data": None
    }

    log_and_assert(response, expected_status_code, expected_values)


def test_delete_user_non_existent():
    """Test case for deleting a non-existent user."""
    non_existent_user_id = 999999
    response = requests.delete(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
    response_json = response.json()

    log_response_data(response, step_name="Delete Invalid User")
    
    expected_status_code=200
    expected_values = {
        "code": 404,
        "meta": None,
        "data": {
            "message": "Resource not found"
        }
    }

    log_and_assert(response, expected_status_code, expected_values)

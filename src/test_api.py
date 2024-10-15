import requests
import pytest
from utils.utils import generate_random_email, generate_random_name, get_random_gender, get_random_status
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
    
    response = requests.post(f"{BASE_URL}/users", json={
        "name": name,
        "email": email,
        "gender": gender,
        "status": status
    }, headers=headers)
    
    return response

def test_create_user_positive(create_user):
    """Test case for creating a new user - positive case."""
    response_json = create_user.json()
    
    assert create_user.status_code == 200, "Expected status code 200 for successful user creation."
    assert response_json["code"] == 201, "Expected 'code' in response to be 201."
    assert response_json["meta"] is None, "Expected 'meta' to be None."
    
    data = response_json["data"]
    assert "id" in data, "Expected 'id' in response data."
    assert data["name"] is not None, "Expected 'name' in response data."
    assert data["email"] is not None, "Expected 'email' in response data."
    assert data["gender"] in ["male", "female"], "Expected 'gender' to be either 'male' or 'female'."
    assert data["status"] in ["active", "inactive"], "Expected 'status' to be either 'active' or 'inactive'."

def test_get_user_details(create_user):
    """Test case for getting user details."""
    user_id = create_user.json()["data"]["id"]
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    response_json = response.json()

    assert response.status_code == 200, "Expected status code 200 for successful retrieval of user details."
    assert response_json["code"] == 200, "Expected 'code' in response to be 200."
    assert response_json["meta"] is None, "Expected 'meta' to be None."
    
    data = response_json["data"]
    assert data["id"] == user_id, "User ID in response should match the requested ID."

def test_get_user_details_non_existent():
    """Test case for getting details of a non-existent user."""
    non_existent_user_id = 999999  # Assuming this user ID does not exist
    response = requests.get(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
    response_json = response.json()

    assert response.status_code == 200, "Expected status still 200 even if trying to get non-existent user's detail."
    assert response_json["code"] == 404, "Expected 'code' in response to be 404 for non-existent user."

def test_update_user_invalid_gender(create_user):
    """Test case for updating user details with an invalid gender."""
    user_id = create_user.json()["data"]["id"]
    update_fields_invalid = {"gender": "not_a_gender"}
    
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_fields_invalid, headers=headers)
    response_json = response.json()
    
    assert response.status_code == 200, "Expected status code 422 even if the gender is not valid."
    assert response_json["code"] == 422, "Expected 'code' in response to be 422 because the gender is not in valid form."

def test_delete_user(create_user):
    """Test case for deleting a user."""
    user_id = create_user.json()["data"]["id"]
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    response_json = response.json()
    
    assert response.status_code == 200, "Expected status code 200 for successful deletion."
    assert response_json["code"] == 204, "Expected 'code' in response to be 204 because a user is successfully deleted."


def test_delete_user_non_existent():
    """Test case for deleting a non-existent user."""
    non_existent_user_id = 999999
    response = requests.delete(f"{BASE_URL}/users/{non_existent_user_id}", headers=headers)
    response_json = response.json()
    
    assert response.status_code == 200, "Expected status code 200 even if trying to delete a non-existent user."
    assert response_json["code"] == 404, "Expected 'code' in response to be 404 because the user doesn't exist."

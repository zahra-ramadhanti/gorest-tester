import allure

def log_request_data(data, step_name="Request Body"):
    """Log request data with Allure."""
    with allure.step(f"Logging {step_name}"):
        allure.attach(str(data), name=step_name, attachment_type=allure.attachment_type.JSON)

def log_response_data(response, step_name="Response"):
    """Log response data with Allure."""
    with allure.step(f"Logging {step_name}"):
        allure.attach(str(response.json()), name=step_name, attachment_type=allure.attachment_type.JSON)

def log_and_assert(response, expected_status, expected_values):
    """
    Log response and assert expected values.

    Parameters:
    - response: The HTTP response object.
    - expected_status: The expected HTTP status code.
    - expected_values: A dictionary of expected values to assert in the response JSON.
    """

    log_response_data(response)
    response_json = response.json()
    
    assert response.status_code == expected_status, f"Expected status code {expected_status}, got {response.status_code}."

    for key, expected_value in expected_values.items():
        actual_value = response_json.get(key)
        assert actual_value == expected_value, f"Expected '{key}' to be {expected_value}, got {actual_value}."

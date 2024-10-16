
# GOREST API Testing with Pytest

## Overview

This project is designed to perform automated testing on the Gorest API using Pytest. It includes various test cases for user management, such as creating, retrieving, updating, and deleting users. The tests are structured to ensure that all functionalities are working correctly and to validate that the API responds as expected.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Tests Description](#tests-description)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Viewing Test Reports](#viewing-test-reports)

## Tests Description
The tests cover the following functionalities:

- Create User: Tests for creating a new user, including edge cases such as email already taken.
- Get User Details: Verifies user details retrieval for valid and non-existent users.
- Update User: Tests updating user details, including invalid cases for gender and status.
- Delete User: Tests deleting users, including edge cases for non-existent users.
- Each test is structured to log request and response data for better debugging and traceability, using Allure for enhanced reporting.

## Prerequisites

Make sure you have the following installed:

- **Python 3.6 or later**
- **pip** (Python package manager)

You can check your Python version by running:

```bash
python --version
```
## Setup
1. Clone repository
```
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate
# On Windows use `venv\Scripts\activate`
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variable
Create a .env file in the root directory of your project and add your API token of GOREST by checking:
```
https://gorest.co.in/my-account/access-tokens
```
get the token, and replace your API_TOKEN in the .env file
```bash
API_TOKEN=your_api_token_here
```

Install allure for reporting purposes in your local device:

- For macOS (using Homebrew)
    ```bash
    brew install allure
    ```

- For Linux:
    ```bash
    sudo apt install allure
    ```

- For Windows:
  - Download the latest Allure Commandline zip from the Allure Releases page : [Allure Installation](https://github.com/allure-framework/allure2/releases)
  - Unzip the downloaded file and add the bin directory to your system's PATH environment variable.

After installing Allure, you can verify that it’s installed correctly by running:
```bash`
allure --version
```
This command should display the installed version of Allure.

## Running Tests
Make sure you already have allure installed on your device, and run
```bash
pytest --cov=src --cov-report=term-missing --html=report.html --alluredir=allure-results -v src/test_api.py
```

## Viewing Test Reports
After running the tests, an HTML report will be generated as report.html in your project directory. You can open this file in your web browser to view the detailed test results.

Viewing Allure Reports
To view the Allure report, you need to have Allure installed. Once Allure is surely installed, you can serve the report with the following command
```bash
allure serve allure-results
```
This command will start a local server and open the Allure report in your default browser.
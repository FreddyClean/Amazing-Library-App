import requests

API_URL = 'https://amazing-library-app-2.onrender.com/'  # Base URL of the API

def login_user(username, password):
    """Send a POST request to the login endpoint."""
    try:
        response = requests.post(f'{API_URL}/login', json={'username': username, 'password': password})
        return response.status_code == 200  # Return True if login was successful
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return False

def sign_up_user(username, password):
    """Send a POST request to the registration endpoint."""
    try:
        response = requests.post(f'{API_URL}/register', json={'username': username, 'password': password})
        return response.status_code == 200  # Return True if sign-up was successful
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return False
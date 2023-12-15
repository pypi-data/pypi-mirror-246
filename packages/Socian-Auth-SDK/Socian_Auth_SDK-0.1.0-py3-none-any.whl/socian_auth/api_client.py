# socian_auth/api_client.py
import requests


class SocianAuthApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_info(self, user_id):
        endpoint = f"{self.base_url}/user/{user_id}"
        response = requests.get(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")

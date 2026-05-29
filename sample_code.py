import json
import requests


class UserAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        data = response.json()
        return data

    def create_user(self, name, email, age):
        payload = {"name": name, "email": email, "age": age}
        response = requests.post(f"{self.base_url}/users", json=payload)
        return response.status_code

    def delete_user(self, user_id):
        requests.delete(f"{self.base_url}/users/{user_id}")
        return True

    def parse_json_response(self, text):
        data = json.loads(text)
        return data


# Usage
api = UserAPI("https://api.example.com")
user = api.get_user(123)
print(user)

api.create_user("john", "john@example.com", 25)
api.delete_user(456)

parsed = api.parse_json_response('{"invalid json}')  # BUG: Will crash
print(parsed)

import requests

data = {"username": "admin1", "password": "admin", "isRememberMe": "false"}
response = requests.post("http://localhost:45555/login?from=/", json=data)
print(response.text)
print(response.cookies.get_dict())
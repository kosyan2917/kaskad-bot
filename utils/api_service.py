import requests

class APIService:

    url = "http://127.0.0.1:45555/"
    def __init__(self):
        pass

    def make_pass_for_taxi(self, number: str) -> bool:
        return True
    
    def make_path(self, number: str, type: str) -> bool:
        return True
    
    def check_login_data(self, login: str, password: str) -> bool:
        return login == "admin" and password=="admin"

    def get_session(self, login: str, password: str) -> str:
        return "sdmfkasdfkjm"
    
    def get_vehicle_types(self) -> list[str]:
        pass

from db_handler.db_interface import DB
import requests
from dataclasses import dataclass

@dataclass
class VehicleInfo:
    plate: str
    vehicle_type: str
    end_time: str


class IncorrectLoginData(Exception):
    pass

class NotOKAnswer(Exception):
    pass

class APIService:

    url = "http://127.0.0.1:45555/"
    def __init__(self, db: DB):
        self.db = db
    
    def make_pass(self, user: str, number: str, type: str) -> bool:
        return True
    
    def check_login_data(self, login: str, password: str) -> bool:
        try:
            self.login(login, password)
            return True
        except Exception as e:
            print(e)
            return False
    
    async def get_vehicle_types(self, user) -> list[str]:
        login, password = self.db.get_login_data(user)
        session = await self.login(login, password)
        cookies = {"s": session}
        response = requests.get("http://localhost:45555/api/v1/vehicletypes", cookies=cookies)
        response = response.json()
        return [vehicle_type["name"] for vehicle_type in response]

    async def get_pass_list(self, user: str) -> list[VehicleInfo]:
        result = []
        login, password = self.db.get_login_data(user)
        session = await self.login(login, password)
        cookies = {"s": session}
        response = requests.get("http://localhost:45555/api/v1/guestslist/records?offset=0&count=22&passStatus=", cookies=cookies)
        response = response.json()["entries"]
        for vehicle in response:
            plate = vehicle["plate"]
            vehicle_type = vehicle["vehicleType"]["name"]
            end_time = vehicle["passes"][0]["schedules"][0]["endTime"]
            vehicle_info = VehicleInfo(plate, vehicle_type, end_time)
            result.append(vehicle_info)
        return result

    async def login(self, login: str, password: str) -> str:
        body = {
            "username": login, "password": password, "isRememberMe": "false"
        }
        response = requests.post(f"{self.url}login?from=/", json=body)
        print(response.status_code)
        if response.status_code != 200:
            raise NotOKAnswer
        if response.json()["isAutorized"] != True:
            raise IncorrectLoginData
        return response.cookies.get_dict()["s"]

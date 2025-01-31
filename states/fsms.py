from aiogram.fsm.state import State, StatesGroup

class LoginStates(StatesGroup):
    login = State()
    password = State()

class PassStates(StatesGroup):
    vehicle_number = State()
    vehicle_type = State()
    confirm = State()

from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    login = State()
    password = State()
    main = State()
    make_pass = State()
    vehicle_number = State()
    vehicle_type = State()
    taxi = State()
    taxi_image = State()
    redact_taxi_number = State()


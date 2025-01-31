from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.fsms import LoginStates
from create_bot import api_service, state_manager, db


login_router = Router()
# login_router.message.outer_middleware(state_manager)

@login_router.message(LoginStates.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await message.answer("Отлично, теперь введите пароль")
    await state.set_state(LoginStates.password)

@login_router.message(LoginStates.password)
async def process_password(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    await state.update_data(password=message.text)
    data = await state.get_data()
    login = data["login"]
    password = data["password"]
    if api_service.check_login_data(login, password):
        if db.set_login_data(user, login, password):
            await state.clear()
            await message.answer("Данные верны, теперь вам доступен основной функционал")
            await state_manager.set_state(user, state_manager.main, message)
        else:
            await state.set_state(LoginStates.login)
            await message.answer("Произошла ошибка при обращении к базе данных. Попробуйте пройти процесс авторизации снова")
            await state_manager.set_state(user, state_manager.unauthorized, message)

    else:
        await state.set_state(LoginStates.login)
        await message.answer("Данные не верны, попробуйте пройти процесс авторизации снова")
        await state_manager.set_state(user, state_manager.unauthorized, message)


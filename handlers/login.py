from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import UserStates
from create_bot import db, api_service, user_sessions


login_router = Router()

@login_router.message(UserStates.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await message.answer("Отлично, теперь введите пароль")
    await state.set_state(UserStates.password)

@login_router.message(UserStates.password)
async def process_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    #TODO: Изменить на корректную проверку логина и пароля с помозью авторизации в реальном сервисе
    data = await state.get_data()
    login = data["login"]
    password = data["password"]
    if api_service.check_login_data(login, password):
        await message.answer("Данные верны. Теперь вам доступен основной функционал")
        if not db.set_login_data(str(message.from_user.id), login, password):
            await message.answer("Ошибка при обращении к бд. Попробуйте ввести данные снова. Сначала логин")
            await state.set_state(UserStates.login)
        else:
            try:
                session = api_service.get_session(login, password)
                user_sessions[message.from_user.id] = session
                await state.set_state(UserStates.main)
            except Exception as e:
                print(e)
                await message.answer("Ошибка при получении сессии. Попробуйте авторизоваться еще раз. Введите логин")
                await state.set_state(UserStates.login)
    else:
        await message.answer("Данные не верны. Давайте попробуем еще раз. Введите логин от учетной записи Automarshal")
        await state.set_state(UserStates.login)

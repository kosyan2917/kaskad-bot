from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import UserStates
from create_bot import db, api_service, user_sessions

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(UserStates.login)
    await message.answer('Для начала необходимо настроить вашу учетную запись для дальнейшей работы. Введите логин от вашей учетной записи automarshal.')

@start_router.message(StateFilter(None))
async def handle_stateless(message: Message, state: FSMContext) -> None:
    if db.check_user(message.from_user.id):
        session = api_service.get_session(*db.get_login_data(message.from_user.id))
        user_sessions[message.from_user.id] = session
        await message.answer("Сделай вид, что я тебе отправил клавиатуру")
        await state.set_state(UserStates.main)
    else:
        await message.answer("Ваш пользователь не найден в базе. Пожалуйста, введите логин от вашей учетной записи Automarshal")
        await state.set_state(UserStates.login)
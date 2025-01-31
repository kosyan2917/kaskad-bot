from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.fsms import LoginStates
from create_bot import db, api_service, state_manager
from middlewares.state_middleware import StateMiddleware

start_router = Router()
start_router.message.outer_middleware(StateMiddleware())

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LoginStates.login)
    await state_manager.set_state(message.from_user.id, state_manager.unauthorized, message)
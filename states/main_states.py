from states.states_interface import State
from aiogram.types import Message
from keyboards.main_keyboard import main_kb

class UnauthorizedState(State):
    async def on_enter(self, message: Message) -> None:
        await message.answer("Введите логин от аккаунта automarshal")

class MainState(State):
    async def on_enter(self, message: Message) -> None:
        await message.answer("Используйте клавиатуру для взаимодействия с ботом", reply_markup=main_kb())

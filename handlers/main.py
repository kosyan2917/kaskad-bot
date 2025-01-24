from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import UserStates
from create_bot import db, api_service
from utils.parse_screenshot import parse_vehicle_number

main_router = Router()

@main_router.message(UserStates.main, F.text.casefold()=="Заказать пропуск")
async def handle_pass(message: Message, state: FSMContext) -> None:
    await message.answer("Введите номер машины")
    await state.set_state(UserStates.vehicle_number)

@main_router.message(UserStates.main, F.text.casefold()=="Заказть пропуск для такси по скриншоту")
async def handle_taxi(message: Message, state: FSMContext) -> None:
    await message.answer("Пришлите скриншот из яндекс.такси")
    await state.set_state(UserStates.taxi_image)

@main_router.message(UserStates.taxi_image, F.text)
async def handle_taxi_text(message: Message, state: FSMContext) -> None:
    await message.answer("Нужно прислать скриншот из приложения яндекс.такси")

@main_router.message(UserStates.taxi_image, F.photo)
async def hande_taxi_image(message: Message, state: FSMContext) -> None:
    number = parse_vehicle_number()
    if number:
        await message.answer(f"На картинке найден номер машины - {number}. Он верный?")
        await state.set_state(UserStates.taxi)
    else:
        await message.answer("На картинке не найден номер машины. Попробуйте отправить другую картинку")

@main_router.message(UserStates.taxi, F.text.casefold()=="Подтвердить")
async def handle_taxi_confirm(message: Message, state: FSMContext):
    login, password = db.get_login_data(message.from_user.id)
    if api_service.make_pass_for_taxi(login, password):
        await message.answer("Пропуск успешно выписан")
    else:
        await message.answer("Произошла ошибка, пропуск не был выписан") 
    await state.set_state(UserStates.main)

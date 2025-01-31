from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.fsms import LoginStates, PassStates
from create_bot import db, api_service, state_manager
from utils.parse_screenshot import parse_vehicle_number
from states.main_states import MainState, UnauthorizedState
from utils.api_service import NotOKAnswer, IncorrectLoginData
import re

main_router = Router()

@main_router.message(F.text.casefold()=="изменить данные для авторизации")
async def process_change_login_data(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    print(db.delete_login_data(user))
    await state.set_state(LoginStates.login)
    await state_manager.set_state(user, state_manager.unauthorized, message)

@main_router.message(F.text.casefold()=="посмотреть активные пропуски")
async def process_pass_list(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    try:
        passes = await api_service.get_pass_list(user)
        await message.answer("Последние 22 заказанных пропуска:")
        msg = ""
        for vehicle_pass in passes:
            s = f"Номер машины: {vehicle_pass.plate}, Тип ТС: {vehicle_pass.vehicle_type}, Пропуск действителен до: {vehicle_pass.end_time} \n _______________ \n"
            msg += s
        print(msg)
        await message.answer(msg)
        await state_manager.set_state(user, state_manager.main, message)
    except NotOKAnswer:
        await message.answer("Сервер не вернул данных")
        await state_manager.set_state(user, state_manager.main)
    except IncorrectLoginData:
        db.delete_login_data(user)
        await message.answer("Ваши логин/пароль не верны. Возвращаю на этап авторизации")
        await state.set_state(LoginStates.login)
        await state_manager.set_state(user, state_manager.unauthorized, message)
    except Exception as e:
        await message.answer(f"Произошла непредвиденная ошибка {repr(e)}")
        await state_manager.set_state(user, state_manager.main, message)

@main_router.message(F.text.casefold()=="отмена", StateFilter(PassStates))
async def cancel(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    await message.answer("Возвращаю на главную. Пропуск не был заказан")
    await state.clear()
    await state_manager.set_state(user, state_manager.main, message)

@main_router.message(F.text.casefold()=="заказать пропуск")
async def make_pass(message: Message, state: FSMContext) -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отмена")
    await message.answer("Введите номер машины", reply_markup=builder.as_markup())
    await state.set_state(PassStates.vehicle_number)

@main_router.message(PassStates.vehicle_number)
async def process_vehicle_number(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    number = message.text
    match = re.search(r"^[A-Za-z]\d{3}[A-Za-z]{2}\d{2,3}$", number)
    if match[0]:
        try:
            vehicle_types = await api_service.get_vehicle_types(user)
            builder = ReplyKeyboardBuilder()
            for typ in vehicle_types:
                builder.button(text=typ)
            builder.button(text="Отмена")
            adjust = [2 for _ in range(0, len(vehicle_types), 2)]
            if len(vehicle_types)%2==1:
                adjust.append(1)
            adjust.append(1)
            builder.adjust(*adjust)
            await state.update_data(vehicle_number=message.text.upper())
            await message.answer("Теперь выберите тип ТС", reply_markup=builder.as_markup(resize_keyboard=True))
            await state.set_state(PassStates.vehicle_type)
        except NotOKAnswer:
            await state.clear()
            await message.answer("Сервер не вернул данных. Пропуск не был заказан")
            await state_manager.set_state(user, state_manager.main)
        except IncorrectLoginData:
            await state.clear()
            db.delete_login_data(user)
            await message.answer("Ваши логин/пароль не верны. Возвращаю на этап авторизации")
            await state.set_state(LoginStates.login)
            await state_manager.set_state(user, state_manager.unauthorized, message)
        except Exception as e:
            await state.clear()
            await message.answer(f"Произошла непредвиденная ошибка {repr(e)}. Пропуск не был заказан")
            await state_manager.set_state(user, state_manager.main, message)

@main_router.message(PassStates.vehicle_type)
async def process_vehicle_type(message: Message, state: FSMContext) -> None:
    # user = message.from_user.id
    await state.update_data(vehicle_type=message.text)
    data = await state.get_data()
    number = data["vehicle_number"]
    type = data["vehicle_type"]
    builder = ReplyKeyboardBuilder()
    builder.button(text="Подтвердить")
    builder.button(text="Отмена")
    builder.adjust(1,1)
    await state.set_state(PassStates.confirm)
    await message.answer(f"Вы заказываете пропуск для машины с типом ТС {type} и номером {number}. Подтвердите ввод",
                         reply_markup=builder.as_markup(),
                         one_time_keyboard=False)
    
@main_router.message(PassStates.confirm, F.text.casefold()=="Подтвердить")
async def process_confirm(message: Message, state: FSMContext):
    user = message.from_user.id
    

@main_router.message(F.text, StateFilter(None))
async def process_stateless_messages(message: Message, state: FSMContext) -> None:
    user = message.from_user.id
    print("Handled by me")
    print(state_manager.get_states())
    if isinstance(state_manager.get_user_state(user), UnauthorizedState):
        await state.set_state(LoginStates.login)
    elif isinstance(state_manager.get_user_state(user), MainState):
        await message.answer("У бота нет такой функции")
        await state_manager.set_state(user, state_manager.main, message)

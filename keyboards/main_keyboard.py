from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def main_kb() -> None:
    kb_list = [
        [KeyboardButton(text="Заказать пропуск")],
        [KeyboardButton(text="Изменить данные для авторизации")],
        [KeyboardButton(text="Посмотреть активные пропуски")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True,
                                   input_field_placeholder="Воспользуйтесь клавиатурой")
    return keyboard
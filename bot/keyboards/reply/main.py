from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class reply_keyboards:

    def all_operations_keyboard(self):
        all_operations_button = KeyboardButton(text='Все операции')

        return ReplyKeyboardMarkup(resize_keyboard=True).add(all_operations_button)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

class inline_keyboards:

    operations_cb = CallbackData('operations_keyboard', 'action')

    def operations_keyboard(self):
        plus_button = InlineKeyboardButton(text='+', callback_data=self.operations_cb.new('+'))
        minus_button = InlineKeyboardButton(text='-', callback_data=self.operations_cb.new('-'))
        multiply_button = InlineKeyboardButton(text='*', callback_data=self.operations_cb.new('*'))
        divide_button = InlineKeyboardButton(text='/', callback_data=self.operations_cb.new('/'))

        return InlineKeyboardMarkup(row_width=1).add(plus_button, minus_button, multiply_button, divide_button)
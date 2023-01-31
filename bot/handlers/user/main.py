from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.keyboards.inline import inline_kb
from bot.keyboards.reply import reply_kb

def register_user_handlers(dp: Dispatcher, db):
    async def send_error_message(message, error_text):
        await message.answer(f"<b>{error_text}</b>")

    async def process_start(message: Message, db):
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await message.answer('<b>Привет!</b>\nЯ бот-калькулятор, для того чтобы произвести операцию'
                             ' <b>введи 2 числа</b>\nПример: 2.13 64',
                             reply_markup=reply_kb().all_operations_keyboard())

    @dp.message_handler(commands=['start', 'help'])
    async def start_handler(message: Message):
        await process_start(message, db)

    @dp.message_handler()
    async def input_data_handler(message: Message, state: FSMContext):
        if message.text == 'Все операции':
            operations = db.get_all_user_operations(message.from_user.id)
            if operations:
                answer = '<b>Список операций</b>\n'
                for operation in operations:
                    answer += f"{operation['first_number']} {operation['operation_type']} {operation['second_number']} = " \
                              f"{operation['answer']}\n"
                await message.answer(answer)
            else:
                await message.answer('<b>Операций не найдено!</b>')
        else:
            async with state.proxy() as data:
                try:
                    numbers = list(map(float, message.text.split()))
                    if len(numbers) != 2:
                        await send_error_message(message, "Количество значений должно равняться 2!")
                    else:
                        data["first_number"] = numbers[0]
                        data["second_number"] = numbers[1]
                        await message.answer('<b>Выбери тип операции!</b>', reply_markup=inline_kb().operations_keyboard())
                except:
                    await send_error_message(message, "Введены некорректные данные!")

    @dp.callback_query_handler(inline_kb().operations_cb.filter())
    async def operations_cb_handler(call: CallbackQuery, callback_data: dict, state: FSMContext):
        async with state.proxy() as data:
            first_number = round(float(data["first_number"]), 2)
            second_number = round(float(data["second_number"]), 2)
            operation = callback_data['action']
            result = None
            if operation == '+':
                result = first_number + second_number
            elif operation == '-':
                result = first_number - second_number
            elif operation == '*':
                result = first_number * second_number
            elif operation == '/':
                result = first_number / second_number
            await call.message.edit_text(f'<b>Ответ</b>\n{first_number} {operation} {second_number} = {round(result, 2)}')
            db.add_operation(call.from_user.id, operation, first_number, second_number, round(result, 2))
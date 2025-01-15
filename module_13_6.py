from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
but = KeyboardButton('Рассчитать')
but2 = KeyboardButton('Информация')
kb.add(but, but2)
kb1 = InlineKeyboardMarkup()
but = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formula')
kb1.add(but, but2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_command(message):
    await message.answer(f'Напишите фразу "Рассчитать" для начала расчета нормы калорий.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    await call.message.answer(f'Ддля мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              f'\nДля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Программа для расчета нормы калорий')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    msj = 10 * weight + 6.25 * growth - 5 * age + 5
    msjm = msj + 5
    msjw = msj - 161
    await message.answer(f'Ваша норма для мужчин: {msjm} ккал в день. \nВаша норма для женщин: {msjw} ккал в день.')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    print(f'Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

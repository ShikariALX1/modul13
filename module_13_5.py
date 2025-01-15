from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
but = KeyboardButton('Рассчитать')
but2 = KeyboardButton('Информация')
kb.add(but, but2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_command(message):
    await message.answer(f'Напишите фразу Calories для начала расчета нормы калорий.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Программа для расчета нормы калорий')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


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

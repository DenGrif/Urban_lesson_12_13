from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'Ключи'

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


dp.middleware.setup(LoggingMiddleware())


# Создаем класс
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обрабатываем команду 'Calories'
@dp.message_handler(Text(equals='Calories', ignore_case=True))
async def set_age(message: Message):
    await UserState.age.set()  # Возраст age
    await message.reply("Введите свой возраст:")


# Обрабатываем ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        age = int(message.text)  # Проверяем введенный возраст на число
        await state.update_data(age=age)  # Сохраняем возраст
        await UserState.growth.set()  # рост
        await message.reply("Введите свой рост (в сантиметрах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для возраста.")


# Обрабатываем ввод роста
@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        growth = int(message.text)  # Проверяем введенный рост на число
        await state.update_data(growth=growth)  # Сохраняем рост
        await UserState.weight.set()  # Переходим к весу
        await message.reply("Введите свой вес (в килограммах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для роста.")


# Обрабатываем ввод веса и вычисляем калории
@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    try:
        weight = int(message.text)  # Проверяем введенный вес на число
        await state.update_data(weight=weight)  # Сохраняем вес

        # Получаем все данные
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        # Пример расчета нормы калорий по формуле Миффлина-Сан Жеора (для мужчин):
        # Калории = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5
        calories = 10 * weight + 6.25 * growth - 5 * age + 5

        # Отправляем результат пользователю
        await message.reply(f"Ваша суточная норма калорий: {calories:.2f} ккал.")

        # Завершаем машину состояний
        await state.finish()
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для веса.")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

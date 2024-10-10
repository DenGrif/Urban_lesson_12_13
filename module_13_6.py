from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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

# Клавиатура с кнопками "Рассчитать" и "Информация"
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton('Рассчитать')
button_info = KeyboardButton('Информация')
keyboard.add(button_calculate, button_info)

# Inline клавиатура с кнопками "Рассчитать норму калорий" и "Формулы расчёта" в одной строке
inline_keyboard = InlineKeyboardMarkup(row_width=2)
button_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard.add(button_calories, button_formulas)  # Добавляем обе кнопки в один ряд

# Команда /start, отправка клавиатуры
@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)

# Нажатие кнопки 'Рассчитать' и делаем Inline меню
@dp.message_handler(Text(equals='Рассчитать', ignore_case=True))
async def main_menu(message: Message):
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)

# Нажатие кнопки 'Формулы расчёта' в Inline меню
@dp.callback_query_handler(Text(equals='formulas'))
async def get_formulas(call: CallbackQuery):
    formulas_text = (
        "Формула Миффлина - Сан Жеора для мужчин:\n"
        "Калории = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n\n"
        "Формула для женщин:\n"
        "Калории = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    )
    await call.message.reply(formulas_text)
    await call.answer()  # Закрываем кнопку

# Нажатие кнопки 'Рассчитать норму калорий' в Inline меню
@dp.callback_query_handler(Text(equals='calories'))
async def set_age(call: CallbackQuery):
    await UserState.age.set()  # Устанавливаем возраст
    await call.message.reply("Введите свой возраст:")
    await call.answer()  # Закрываем кнопку

# Ввод возраста
@dp.message_handler(state=UserState.age)
async def set_growth(message: Message, state: FSMContext):
    try:
        age = int(message.text)  # Введенный возраст на число
        await state.update_data(age=age)  # Сохраняем возраст
        await UserState.growth.set()  # Переходим к росту
        await message.reply("Введите свой рост (в сантиметрах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для возраста.")

# Переходим к росту
@dp.message_handler(state=UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    try:
        growth = int(message.text)  # Введенный рост на число
        await state.update_data(growth=growth)  # Сохраняем рост
        await UserState.weight.set()  # Переходим к весу
        await message.reply("Введите свой вес (в килограммах):")
    except ValueError:
        await message.reply("Пожалуйста, введите корректное число для роста.")

# Ввод веса и вычисляем калории
@dp.message_handler(state=UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    try:
        weight = int(message.text)  # Введенный вес на число
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

# Нажатие кнопки 'Информация'
@dp.message_handler(Text(equals='Информация', ignore_case=True))
async def send_info(message: Message):
    info_text = (
        "Этот бот помогает вам рассчитать суточную норму калорий "
        "с использованием формулы Миффлина - Сан Жеора. Для этого нужно "
        "ввести свои данные: возраст, рост и вес."
    )
    await message.reply(info_text)

# Ввод любого текста вызывает функцию 'Информация'
@dp.message_handler()
async def handle_any_text(message: Message):
    await send_info(message)  # Вызываем функцию send_info для ответа

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

from crud_functions import initiate_db, get_all_products

API_TOKEN = '8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI'

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())

initiate_db()

# Словарь для картинок
product_images = {
    "Игра 1": "Lgame.jpg",
    "Игра 2": "Mgame.jpg",
    "Игра 3": "XLgame.jpg",
    "Игра 4": "XXLgame.jpg"
}

# Клава с кнопками "Информация" и "Купить"
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton('Информация')
button_buy = KeyboardButton('Купить')
keyboard.add(button_info, button_buy)

inline_buy_keyboard = InlineKeyboardMarkup(row_width=2)

# Загрузка из базы данных
products_from_db = get_all_products()

for product in products_from_db:
    product_name = product[1]
    inline_buy_keyboard.add(
        InlineKeyboardButton(product_name, callback_data=str(product[0])))  # Используем ID как callback_data

# Клавиатура с кнопкой "Назад"
inline_back_keyboard = InlineKeyboardMarkup(row_width=1)
back_button = InlineKeyboardButton('Назад', callback_data='back')
inline_back_keyboard.add(back_button)


# /start
@dp.message_handler(commands=['start'])
async def start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name
    await message.reply(
        f"Добро пожаловать, {full_name}! 😉\n Посмотрите информацию о наших играх, кнопка: 'Информация', выбирайте - кнопка: 'Купить'",
        reply_markup=keyboard
    )


# "Купить"
@dp.message_handler(Text(equals='Купить', ignore_case=True))
async def get_buying_list(message: Message):
    # Выводим спискок с их информацией
    products = get_all_products()
    product_list = "\n".join([f"Название: {p[1]} | Описание: {p[2]} | Цена: {p[3]} руб." for p in products])

    await message.reply(f"Список продуктов:\n{product_list}", reply_markup=inline_buy_keyboard)


# Покупка продуктов и вывод картинок
@dp.callback_query_handler(lambda call: call.data.isdigit())
async def send_product_image(call: CallbackQuery):
    # По ID
    product_id = int(call.data)
    products = get_all_products()
    selected_product = next((p for p in products if p[0] == product_id), None)

    if selected_product:
        product_title = selected_product[1]

        # Путь к картинке из словаря
        product_image_path = product_images.get(product_title, None)

        if product_image_path:
            # Отправляем картинку
            with open(product_image_path, 'rb') as photo:
                await call.message.reply_photo(photo, caption=f"Вы выбрали {product_title}. Отличный выбор! 😉")
        else:
            await call.message.reply("Изображение для этого продукта не найдено.")

    # Добавляем кнопку "Назад"
    await call.message.reply("Вернуться назад к выбору продуктов:", reply_markup=inline_back_keyboard)
    await call.answer()


# Для кнопки "Назад"
@dp.callback_query_handler(lambda call: call.data == 'back')
async def go_back(call: CallbackQuery):
    # Возвращаемся к выбору продуктов
    await call.message.edit_text("Выберите продукт для покупки:", reply_markup=inline_buy_keyboard)
    await call.answer()


# Кнопка "Информация"
@dp.message_handler(Text(equals='Информация', ignore_case=True))
async def send_info(message: Message):
    info_text = (
        "Мы продаём лучшие игры уже 2000 лет, но вы нам не поверите, поэтому скажем, что два дня"
    )
    await message.reply(info_text)

    with open('About.jpg', 'rb') as photo:
        await message.reply_photo(photo)


# /start для любого другого текста
@dp.message_handler()
async def handle_any_text(message: Message):
    await message.reply("Нажимай на /start, чтоб запустить бота")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

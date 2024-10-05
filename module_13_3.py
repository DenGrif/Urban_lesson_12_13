from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


api = "Ключ"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['Urban', 'ff'])
async def handle_urban_message(message: types.Message):
    await message.answer("Urban message")


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Мы рады вас видеть в нашем боте! Он мне ответил!")


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer(f"Мы получили сообщение: {message.text}. Он мне ответил!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

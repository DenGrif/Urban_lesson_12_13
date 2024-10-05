from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "8008288734:AAF9GenuyNrCuauqNPt32HMr_RCYr31VbbI"
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(text=['Urban', 'ff'])
async def start_massage(massage):
    print("Urban massage")
    await massage.answer("Urban massage")


@dp.message_handler(commands=['start'])
async def start_massage(massage):
    print("Start massage")
    await massage.answer("Мы рады вас видеть в нашем боте")

@dp.message_handler()
async def all_massage(massage):
    print("Мы получили сообщение")
    await massage.answer(massage.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
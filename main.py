import asyncio, logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from content import API_KEY, users
from models import Update, SendNewPosts

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_KEY)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['status'])
async def start(message: types.Message):
    await message.answer('Вроде все работает')

async def on_startup(x):
    msg = SendNewPosts(bot, users)
    asyncio.create_task(Update.update_yandex_posts())
    asyncio.create_task(Update.update_avito_posts())
    asyncio.create_task(Update.update_vk_posts())
    asyncio.create_task(msg.send_new_posts())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, relax=60, on_startup=on_startup)

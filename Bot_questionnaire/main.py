import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
import commands
import questionnaire
from aiogram.enums.content_type import ContentType

bot = Bot(token="6775658889:AAFXm-n-2RrFPMQ64tFwbmZ46UnIxFqlGU8")

async def main():
    dp = Dispatcher()
    dp.include_routers(commands.router, questionnaire.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
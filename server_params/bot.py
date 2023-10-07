import datetime

from aiogram import Bot

bot = Bot(token=config.bot_token)


async def send_message(error_text: str):
    await bot.send_message(chat_id=config.dev_chat_id,
                           text=f"""{datetime.datetime.now()} произошла ошибка на сервере.
                           Содержимое ошибки:
                           
                           {error_text}""")

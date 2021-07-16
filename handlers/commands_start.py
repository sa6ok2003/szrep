from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    from .callbak_data import name_channel_1, name_channel_2, name_channel_3
    channel_name = message.text[12:]
    ref = message.text[7:12]

    reg_user(message.chat.id,channel_name,ref)

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='✅ Я ПОДПИСАЛСЯ', callback_data=f'check{channel_name}')
    markup.add(bat_a)

    await bot.send_message(message.chat.id, f"""
<b>❌ ДОСТУП ЗАКРЫТ ❌</b>

👉Для скачивания и просмотра фильмов необходимо подписаться на ниже указанные каналы.

После этого жми кнопку <b>Я ПОДПИСАЛСЯ</b> для проверки!

<b>Канал 1</b> - https://t.me/{name_channel_1}
<b>Канал 2</b> - https://t.me/{name_channel_2}
<b>Канал 3</b> - https://t.me/{name_channel_3}""",parse_mode='html',reply_markup=markup,disable_web_page_preview=True)


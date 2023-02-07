from aiogram import types

from send_msg import bot

# Reply Keyboard для отправки локации
markup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False
)
location = types.KeyboardButton("Отправить локацию", request_location=True)
markup.add(location)

# Убрать Reply Keyboard
hide_kb = types.ReplyKeyboardRemove()


async def edit_reply_markup(
    chat_id: int, msg_id: int, reply_markup: types.ReplyKeyboardMarkup
) -> types.Message:
    """Добавляем Inline keyboard"""
    await bot.edit_message_reply_markup(
        chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup
    )

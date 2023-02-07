from aiogram import types

from bot_settings import bot


async def send_text(
    message: types.Message, text: str,
    reply_markup: types.ReplyKeyboardMarkup = None,
    parse_mode: types.ParseMode = 'markdown'
) -> types.Message:
    """Отправляем текстовое сообщение в ответ"""
    await message.answer(
        text=text, reply_markup=reply_markup, parse_mode=parse_mode
    )


async def send_photo(
    message: types.Message, img: types.InputMediaPhoto,
    reply_markup: types.ReplyKeyboardMarkup = None
) -> types.Message:
    """Отправляем фото"""
    await message.answer_photo(photo=img, reply_markup=reply_markup)


async def send_reply_text(
    chat_id: int, text: str, reply_to_message_id: int,
    reply_markup: types.ReplyKeyboardMarkup = None,
    parse_mode: types.ParseMode = 'markdown'
) -> types.Message:
    """Ответ на запрос о подсказке"""
    await bot.send_message(
        chat_id, text, reply_to_message_id=reply_to_message_id,
        reply_markup=reply_markup, parse_mode=parse_mode
    )

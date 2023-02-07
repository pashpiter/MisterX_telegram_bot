from aiogram import types

from send_msg import send_reply_text


async def help_loc_3(message: types.Message) -> None:
    """Подсказка для задания на локации 3"""
    await send_reply_text(
        message.chat.id, 'Используй круглый дешифратор из конверта. Нужно '
        'чтобы сердечки на обоих кругах совпали и тогда каждая цифра будет '
        'обозначать нужную букву', message.message_id
    )
    await message.edit_reply_markup()


async def help_loc_4(message: types.Message) -> None:
    """Подсказка для задания на локации 8"""
    await send_reply_text(
        message.chat.id, 'Попробуй прочитать слово так, как бы его стал читать'
        ' араб 👳', message.message_id
    )
    await message.edit_reply_markup()


async def help_loc_5(message: types.Message) -> None:
    """Подсказка для задания на локации 5"""
    await send_reply_text(
        message.chat.id, 'Используй уже полученное *"слово для шифра"* из '
        'второй локации - это _буквы ключа_ в шифре Виженера(большая таблица с'
        ' буквами) и слово *ПБЩЬДЧ* - это те буквы, которые нужно искать в '
        'таблице. Берешь первую букву ключа, находишь первую букву '
        'зашифрованного слова и получаешь первую букву исходного текста. И так'
        ' с каждой буквой. Все _буквы исходного текста_ и будут вторым кодовым'
        ' словом', message.message_id
    )
    await message.edit_reply_markup()


async def help_loc_8(message: types.Message) -> None:
    """Подсказка для задания на локации 8"""
    await send_reply_text(
        message.chat.id, 'Попробуй использовать первые буквы каждой строки '
        'чтобы составить последнее ключевое слово', message.message_id
    )
    await message.edit_reply_markup()

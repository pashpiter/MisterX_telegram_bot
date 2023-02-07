from aiogram import types

from bot_settings import logging
from send_msg import send_photo, send_text


async def task_location_seven(message: types.Message, key: str) -> None:
    """Задание для седьмой локации"""
    voc = {
        'st': 'Нет, не верно, попробуй ещё раз',
        'pl': 'Нет, не он, попробуй ещё раз',
        'sel': 'Нет, не верно, попробуй ещё раз',
        'photo': 'Нет, не он, попробуй ещё раз',
        'waiter': 'Точно! Это официант. Левше удобнее нести поднос в правой '
                  'руке, а расставлять еду и напитки левой, так как ведущая '
                  'рука работает, а другая просто зафиксирована.'
    }
    await send_text(message, voc[key])
    if key == 'waiter':
        await send_text(
            message, 'И вот что нам известно:\n*В следующей локации нужно '
            'будет найти последнее ключевое слово* Следуй в *дом Трех Бенуа*, '
            'по адресу *Каменноостровский проспект 26-28* и найди там *двор '
            '#4*'
        )
        await message.edit_reply_markup()


async def task_location_nine(message: types.Message, key: str) -> None:
    """Задание для девятой локации"""
    voc = {
        'tamila': 'Нет, это точно не она. Попробуй ещё раз',
        'jhon': 'Похоже что это не он. Попробуй ещё раз',
        'kevin': 'Он бы наверно не пошел на такое. Попробуй ещё раз',
        'bill': 'Да, точно, если перевернуть цифры _7718_ то можно увидеть имя'
                ' перступника - *Билл*.'
    }
    await send_text(message, voc[key])
    if key == 'bill':
        logging.info(f'User {message.chat.id}, {message.chat.username}'
                     ' end the quest after location 9')
        await message.edit_reply_markup()
        await send_text(
            message, 'Теперь он от нас не уйдет! Спасибо большое за помощь! '
            'На этом квест подошел к концу 🥺'
        )
        await send_text(message, 'До новых встреч!')
        await send_photo(
            message, 'https://www.dropbox.com/s/cwhxxsa384prcu1/unnamed.jpg'
        )

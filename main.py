from aiogram import asyncio, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import database as db
from bot_settings import CODE_WORDS, ID_MY, dp, logging
from func_for_admin import log_answer
from help_loc import help_loc_3, help_loc_4, help_loc_5, help_loc_8
from locations import (location_eight, location_five, location_four,
                       location_nine, location_one, location_seven,
                       location_six, location_three, location_two)
from markups import markup
from send_msg import bot, send_photo, send_reply_text, send_text
from tasks import task_location_nine, task_location_seven


class Form(StatesGroup):
    """Класс для отлавливания сообщений"""
    answer = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> types.Message:
    """Приветствие"""
    await message.reply(
        text=f'Привет {message.chat.username}! '
        'Нужно кодовое слово, чтобы начать'
    )


@dp.message_handler(lambda message: message.chat.id == ID_MY, commands=['log'])
async def log_command(message: types.Message) -> types.Message:
    """Просмотр логов, доступно только для разработчика"""
    f = open('bot_log.log', encoding='UTF-8')
    log = [line for line in f]
    f.close()
    k = {
        'log_5': 5, 'log_10': 10, 'log_15': 15,
        'log_20': 20, 'log_25': 25, 'log_30': 30
    }
    kb = types.InlineKeyboardMarkup()
    buttons = []
    for keys, values in k.items():
        buttons.extend([types.InlineKeyboardButton(
            text=values, callback_data=keys
        )])
    kb.add(*buttons)
    await message.reply(f'Количество логов: {len(log)}', reply_markup=kb)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message) -> types.Message:
    """Помощь"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'asking for help')
    await Form.answer.set()
    key_help = types.InlineKeyboardButton(
        text='Отмена', callback_data='cancel'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await send_reply_text(
        message.chat.id, 'Следующуее текстовое сообщение я отправлю '
        'разработчку', message.message_id, kb
    )


@dp.message_handler(state=Form.answer)
async def forward_answer(
    message: types.Message, state: FSMContext
) -> types.Message:
    """Ловим сообщение пользователя после help"""
    logging.info(f'Get request "{message.text}" for help from user '
                 f'{message.chat.id}, {message.chat.username} and send '
                 'forward')
    await message.forward(ID_MY)
    await bot.edit_message_reply_markup(message.chat.id, message.message_id-1)
    await state.finish()


@dp.message_handler(content_types=['location'])
async def get_location(message: types.Message) -> None:
    """Получаем локацию из сообщения и передаем дальше"""
    await choose_location(
        message, message.location.latitude, message.location.longitude
    )


@dp.message_handler(
    lambda message: message.chat.id == ID_MY and message.reply_to_message,
    content_types=['text']
)
async def send_msg_from_me_to_user(message: types.Message) -> None:
    """Ответ от разработчика на пересылаемое сообщение от пользователя"""
    logging.info(f'Reply message "{message.text}" for message '
                 f'"{message.reply_to_message.text}" user '
                 f'{message.reply_to_message.forward_from.id}, '
                 f'{message.reply_to_message.forward_from.username}')
    await bot.send_message(
        message.reply_to_message.forward_from.id, message.text,
        reply_to_message_id=message.reply_to_message.message_id-1
    )


@dp.message_handler(content_types=['text'])
async def get_text(message: types.Message) -> None:
    """Получаем текст из сообщения и передаем дальше"""
    text = message.text.lower()
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 f'send text "{text}"')
    if text in CODE_WORDS:
        await first_message(message)
    elif text == 'наслаждайся каждым моментом':
        await right_code_phrase(message)
    else:
        await send_text(message, 'Не понимаю, что это значит, но я обязательно'
                                 ' передам эту информацию куда следует. Можешь'
                                 ' воспользоваться /help для связи с '
                                 'разработчиком'
                        )


@dp.message_handler(content_types=['sticker'])
async def get_sticker(message: types.Message) -> types.Message:
    """Пересылает обратно полученный стикер"""
    logging.info(f'Get stiker "{message.sticker.emoji}" from '
                 f'"{message.sticker.set_name}" set')
    await message.answer_sticker(message.sticker.file_id, protect_content=True)


@dp.callback_query_handler(
    lambda call: call.data == 'cancel', state=Form.answer
)
async def cancel_callback(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    """Отменяет написание сообщения разработчику"""
    logging.info(f'User {call.message.chat.id}, {call.message.chat.username} '
                 'cancel request for help')
    await state.finish()
    await call.message.delete()


@dp.callback_query_handler(lambda call: True)
async def get_callback(call: types.CallbackQuery) -> None:
    """Обработка callback от Inline Keyboard"""
    if call.data == 'help_loc_3':
        await help_loc_3(call.message)
    elif call.data == 'help_loc_4':
        await help_loc_4(call.message)
    elif call.data == 'help_loc_5':
        await help_loc_5(call.message)
    elif call.data == 'help_loc_8':
        await help_loc_8(call.message)
    elif call.data == 'hochu':
        await hochu(call.message)
    elif call.data == 'nehochu':
        await nehochu_final(call.message)
    elif call.data in ('st', 'pl', 'sel', 'photo', 'waiter'):
        await task_location_seven(call.message, call.data)
    elif call.data in ('tamila', 'jhon', 'bill', 'kevin'):
        await task_location_nine(call.message, call.data)
    elif call.data in (
        'log_5', 'log_10', 'log_15', 'log_20', 'log_25', 'log_30'
    ):
        await log_answer(call.message, call.data)


async def choose_location(
    message: types.Message, lat: float, lon: float
) -> None:
    """Определяем необходимую локацию"""
    if 59.909 <= lat <= 59.914 and 30.304 <= lon <= 30.308:
        text = 'Тестовая локация'
        await send_text(message, text)
    elif 59.9615 <= lat <= 59.9633 and 30.3023 <= lon <= 30.3056:
        await location_one(message)
    elif 59.9578 <= lat <= 59.9584 and 30.2865 <= lon <= 30.2886:
        await location_two(message)
    elif 59.9534 <= lat <= 59.954 and 30.2892 <= lon <= 30.2912:
        await location_three(message)
    elif 59.9554 <= lat <= 59.9562 and 30.298 <= lon <= 30.3:
        await location_four(message)
    elif 59.9518 <= lat <= 59.9529 and 30.2992 <= lon <= 30.3012:
        await location_five(message)
    elif 59.9513 <= lat <= 59.9523 and 30.3054 <= lon <= 30.3071:
        await location_six(message)
    elif 59.9569 <= lat <= 59.9576 and 30.315 <= lon <= 30.317:
        await location_seven(message)
    elif 59.9564 <= lat <= 59.9568 and 30.3203 <= lon <= 30.3217:
        await location_seven(message, second=True)
    elif 59.9614 <= lat <= 59.9624 and 30.3123 <= lon <= 30.3135:
        await location_eight(message)
    elif 59.9704 <= lat <= 59.9711 and 30.3187 <= lon <= 30.3208:
        await location_nine(message)
    else:
        logging.info(f'User {message.chat.id}, {message.chat.username}'
                     f' lat = {lat}, long = {lon}')
        await send_text(message, text='Не похоже что ты на месте')


async def first_message(message: types.Message) -> None:
    """Получаем кодовое слово для начала квеста и отправляем инструкции"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_sname = message.from_user.last_name
    username = message.from_user.username
    check = db.db_table_val(
        user_id=user_id, user_name=user_name,
        user_surname=user_sname, username=username
    )
    if check:
        logging.info(f'User {message.chat.id}, {message.chat.username} '
                     f'add to databse')
    await send_text(
        message, 'Привет! Рад тебя приветствовать!\nТебе предстоит пройти по '
        'пятам _Мистер Х_ и поймать его, пока этот негодяй не скрылся! Для '
        'этого нужно будет собирать подсказки, ключи, решать головоломки, '
        'ребусы, раскрывать шифры и тогда _Мистер Х_ будет повержен.'
    )
    await send_text(
        message, 'Итак, давай приступим. На данный момент у нас уже есть '
        'некоторые перехваченные данные, которые могут пригодится, они '
        'находятся у тебя в конверте. Чтобы начать охоту следуй в *Двор '
        'Нельсона* по адресу *Полозова улица 6*. И не забудь взять конверт и '
        'все что в нем есть!'
    )
    await send_text(
        message, 'Я иногда задумываюсь и могу не ответить сразу. Если ты '
        'отправил(-а) мне сообщение или локацию, а я ничего не ответил, то '
        'отправь это же сообщение (локацию) мне ещё раз, пожалуйста.'
    )
    await send_text(
        message, 'На каждой из локаций есть уникальное место, '
        'достоприпечательность, которую ты также можешь найти и изучить.'
    )
    await send_text(
        message, 'Как прибудешь на каждую из локаций, то отправь свое '
        'местоположение. Для этого есть кнопка ниже *Отправить локацию*. Если '
        'её нет, то смотри её рядом со стикерами, значок квадрата с четырмя '
        'квадратами внутри'
    )
    await send_text(
        message,
        'Как доберешся - отправь свою локацию с помощью кнопки ниже 👇',
        markup
    )


async def right_code_phrase(message: types.Message) -> None:
    """Получена правильная итоговая кодовая фраза"""
    logging.info(f'From {message.chat.id}, {message.chat.username} '
                 'get right code phrase')
    await send_text(
        message, 'Это то что и было нужно! Спасибо за участие в миссии по '
        'поимке _Мистера Х_.'
    )
    await send_text(
        message, 'Если несложно, то напиши отзыв о пройденном квесте по данной'
        ' [ссылке](https://forms.gle/yqGWitPjn5LWiSBM9)'
    )
    await asyncio.sleep(2)
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton('Хочу 🤩', callback_data='hochu'),
        types.InlineKeyboardButton('Не хочу 🧐', callback_data='nehochu')
    )
    await send_text(
        message, 'Если хочешь, то можешь ещё помочь нам вычислить преступника '
        'и решить последнюю задачку.', kb
    )


async def nehochu_final(message: types.Message) -> None:
    """Последнее сообщение после 8-й локации, в случае отрицательного ответа"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'end the quest after location 8')
    await send_text(
        message, 'Хорошо! Спасибо за помощь в поимке _Мистера X_! '
        'Хорошего дня!'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/cwhxxsa384prcu1/unnamed.jpg'
    )
    await message.edit_reply_markup()


async def hochu(message: types.Message) -> None:
    """Продолжение квеста после 8-й локации, в случае положительного ответа"""
    await send_text(
        message, 'Хорошо! Тогда следуй на пересечение '
        '*улицы Профессора Попова* и *Аптекарского проспекта*. Или можно по '
        'адресу *улица Профессора Попова 5*.',
        markup
    )
    await message.edit_reply_markup()


async def edit_reply_markup(
    chat_id: int, msg_id: int, reply_markup: types.ReplyKeyboardMarkup
) -> types.Message:
    """Добавляем Inline keyboard"""
    await bot.edit_message_reply_markup(
        chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

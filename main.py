import logging
import time
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types, asyncio

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ID_MY = os.getenv('MY_ID')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Reply Keyboard для отправки локации
markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
location = types.KeyboardButton("Отправить локацию", request_location=True)
markup.add(location)

# Inline Keyboard
kb = types.InlineKeyboardMarkup()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Приветствие"""
    await message.reply(text=f'Привет {message.chat.username}! Нужно кодовое слово, чтобы начать')


@dp.message_handler(content_types=['location'])
async def get_location(message: types.Message) -> None:
    """Получаем локацию из сообщения и передаем дальше"""
    print(message)
    await choose_location(message, message.location.latitude, message.location.longitude)


@dp.message_handler(content_types=['text'])
async def get_text(message: types.Message) -> None:
    """Получаем текст из сообщения и передаем дальше"""
    text = message.text.lower
    if  text == 'привет':
        await first_message(message)
    elif text == 'наслаждайся каждым моментом':
        pass
    await message.answer(message.text)


@dp.message_handler(content_types=['sticker'])
async def get_sticker(message: types.Message):
    """Пересылает полученный стикер"""
    await message.answer_sticker(message.sticker.file_id)


@dp.callback_query_handler(lambda call: True)
async def get_callback(call):
    """Обработка callback от Inline Keyboard"""
    if call.data == 'help_loc_3':
        await help_loc_3(call.message)
    elif call.data == 'help_loc_4':
        await help_loc_4(call.message)
    elif call.data == 'help_loc_5':
        await help_loc_5(call.message)


async def choose_location(message: types.Message, lat: float, lon: float) -> None:
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
    elif 59.9642 <= lat <= 59.9647 and 30.3108 <= lon <= 30.3118:
        await location_nine(message)
    else:
        await send_text(message, text='Не похоже что ты на месте')


async def location_one(message: types.Message) -> None:
    """Локация 1"""
    await send_text(message, 'Приветствую на первой локации! Это двор Нельсона, неформальная достопримечательность Петроградской стороны')
    await send_text(message, 'И вернемся к делу. Несколько дней назад нам удалось перехватить сообщение _Мистера Х_:\n\n*Одна из подсказок находится по адресу Пионерская улица 22*')
    await send_photo(message, 'https://img.the-village.ru/4kNSEWjYk4QPhPSdbGveLGPr8CnK3wje2OCy3QrTM1Y/rs:fill:620:415/q:88/plain/post-image_featured/Dlk8pFHJKaVBTf3rd8VNrw.png')
    await send_text(message, 'И как прибудешь на локацию - отправь свое местоположение с помощью кнопки ниже 👇', markup)

async def location_two(message: types.Message) -> None:
    """Локация 2"""
    await send_text(message, 'Здесь можно найти замечательное граффити "Покорение неба и космоса"')
    await send_text(message, 'Также по этой геоточке есть следующая информация:\n\nСлово для шифра: *"Датчик"*\n\nДальше следуй во двор по адресу: _Малый проспект П.С. 1Б_')
    await send_photo(message, 'http://risovach.ru/upload/2020/07/mem/hochu-obnimashek_244397878_orig_.jpg')
    await send_text(message, 'Как прибудешь на локацию - отправь свое местоположение с помощью кнопки ниже 👇', markup)


async def location_three(message: types.Message) -> None:
    """Локация 3"""
    await send_text(message, 'Добро пожаловать в восьмиугольный двор колодец!')
    cipher_loc_3 = 'Идём по пятам _Мистера Х_, вот что у нас есть:\n*5 4 30 25 10 4\n 15 14 10 25 10\n33 1 15 14 1 22 24 1 23 15 35*\n\nИ вот ещё:'
    await send_text(message, cipher_loc_3)
    await send_text(message, '*59.955998, 30.298809*')
    await send_photo(message, 'https://lh3.googleusercontent.com/proxy/raysuDMEM2Tpy7JR90Eqf0IGP5St_mOl3G5AlFQEOlfXNllNx9JuCrMa4TEJPmcdWR7-YRzWnccWSUJrZS-EKZaTMDo')
    key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help_loc_3')
    kb.add(key_help)
    await asyncio.sleep(7)
    await edit_msg(message.chat.id ,message.message_id + 2, cipher_loc_3, kb)


async def location_four(message: types.Message) -> None:
    """Локация 4"""
    await send_text(message, 'На углу дома 10 по Большой Пушкарской можно найти памятную табличку с тем, какой уровень воды был в городе в 1924 году')
    cipher_loc_4 = 'Мы только что перехватили сообщение, может быть это локация 🤔🤔🤔:\n\n*яоцароткивревкс*'
    await send_text(message, cipher_loc_4)
    await send_photo(message, 'https://www.dropbox.com/s/avajjz44qfu0bdk/%D0%BF%D0%B8%D0%BA%D0%B0%D1%87%D1%83.jpg')
    await asyncio.sleep(30)
    key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help_loc_4')
    kb.add(key_help)
    await edit_msg(message.chat.id, message.message_id + 2, cipher_loc_4, kb)


async def location_five(message: types.Message) -> None:
    """Локация 5"""
    await send_text(
        message, 'Ты на месте! Это сквер Виктора Цоя. \n _Название скверу '
        'было присвоено 20 сентября 2012 года. Сквер был выбран в связи с тем,'
        ' что певец Виктор Цой трудился неподалеку — в котельной «Камчатка» '
        '(улица Блохина 15, советую зайти в этот двор, это в ста метрах '
        'отсюда). Конструктивно сквер частично расположен на крыше '
        'бомбоубежища на высоте около 1,5 метров относительно окружающего '
        'ландшафта. После присвоения скверу имени Виктора Цоя он не раз '
        'становился площадкой уличных фестивалей._ @wikipedia\nТакже, если '
        'посмотреть на сквер сверху, можно увидеть скрипичный ключ (в '
        'зеркальном отражении).'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/1ltnn9icltrd3xp/%D1%81%D0%BA%D0%B2'
        '%D0%B5%D1%80%20%D0%B2%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%B0%20%D1%86%D0'
        '%BE%D1%8F.jpg')
    cipher_loc_5 = 'Второе ключевое слово: *ПБЩЬДЧ*'
    await send_text(message, cipher_loc_5)
    await send_text(
        message, 'Это все что есть, попробуй использовать те подсказки, '
        'которые у тебя уже есть, чтобы разгадать'
    )
    await asyncio.sleep(10)
    await send_text(
        message, 'Следующая локация Мистера Х находится *на входе в '
        'Экзотариум*'
    )
    await send_photo(
        message, 'https://upload.wikimedia.org/wikipedia/commons/4/4d/Zoo_SPB_'
        'entrance.jpg'
    )
    await asyncio.sleep(40)
    key_help = types.InlineKeyboardButton(text='Помощь', callback_data='help_loc_5')
    kb.add(key_help)
    await edit_msg(message.chat.id, message.message_id + 3, cipher_loc_5, kb)


async def location_six(message: types.Message) -> None:
    """Локация 6"""
    await send_text(
        message, 'Это одни из входов в Ленинградский зоопарк. История зверинца'
        ' начинается в 1865 году, когда любители животных Софья и Юлиус '
        'Гебгардт открыли его в историческом центре города. Затем он сменил '
        'множество частных владельцев и в 1918 году зоосад был '
        'национализирован. Во время Великой Отечественной войны сотрудники '
        'зоосада в тяжелейших условиях не прекращали работу и сохраняли '
        'животных.\nЭто один из серевных зоопарков мира, где содеражтся около '
        '600 видов млекопитающих, птиц, рыб и беспозвоночных из разных уголков'
        ' Земли.'
    )
    await send_text(
        message, 'Итак, вернемся к поиску. У тебя уже есть шифр с квадратами, '
        'расставь на нем фигуры так, чтобы в каждом столбце, строке и в каждом'
        ' квадрате с двойной границей были разные фигуры, как в *судоку*, '
        'только с фигурами. Острие треугольников должны смотреть вверх. Затем '
        'сопоставь судоку с картинкой и треугольники подскажут тебе следующее '
        'место, куда тебе нужно добраться.'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/nnhduqih57oq5x4/%D0%91%D0%B5%D0%B7'
        '%D1%8B%D0%BC%D1%8F%D0%BD%D0%BD%D1%8B%D0%B9%201.jpg'
    )


async def location_seven(message: types.Message, second: bool=False) -> None:
    """Локация 7"""
    if not second:
        await send_text(
            message, 'Правильно! Это и есть та точка! Это постройка 1953 г. о чем '
            'свидетельствует дата на фронтоне.'
        )
    elif second:
        await send_text(
            message, 'Правильно! Это и есть та точка! Это постройка 1879 г., в'
            ' этом доме, в разыне периоды жили: архитектор Г. В. Войневич, а '
            'также композитор, музыкант, автор слов и музыки многих песен О.Д.'
            ' Строк'
        )
    await asyncio.sleep(5)
    await send_text(message, 'Теперь ближе к делу')
    k = {'st': 'Столяр', 'pl': 'Плотник', 'sel': 'Менеджер',
         'photo': 'Фотограф', 'waiter': 'Официант'}
    # kb = types.InlineKeyboardMarkup()
    buttons = []
    for data, text in k.items():
        buttons.extend([types.InlineKeyboardButton(text=text, callback_data=data)])
    kb.add(*buttons)
    await send_text(
        message, 'Мы тут в отделе думаем над одной задачей, помоги нам '
        'пожалуйста и мы поделимся новыми данными.\n*Помоги нам вычислить '
        'левшу.*'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/73ch4ccixxzqh3p/5140025df1b0bbb36e'
        'e37aa933.jpg', kb
    )


async def location_eight(message: types.Message) -> None:
    """Локация 8"""
    text = f'Локация 8 {message.location.latitude}, {message.location.longitude}'
    await send_text(message, text)


async def location_nine(message: types.Message) -> None:
    """Локация 9"""
    text = f'Локация 9 {message.location.latitude}, {message.location.longitude}'
    await send_text(message, text)


async def first_message(message: types.Message) -> None:
    """Получаем кодовое слово для начала квеста и отправляем инструкции"""
    await send_text(message, 'Привет! Рад тебя приветствовать!\nТебе предстоит пройти по пятам _Мистер Х_ и поймать его, пока этот негодяй не скрылся! Для этого нужно будет собирать подсказки, ключи, решать головоломки, ребусы, раскрывать шифры и тогда _Мистер Х_ будет повержен.')
    await send_text(message, 'Итак, давай приступим. На данный момент у нас уже есть некоторые перехваченные данные, которые могут пригодится, они находятся у тебя в конверте. Чтобы начать охоту следуй в *Двор Нельсона* по адресу *Полозова улица 6*. И не забудь взять конверт и все что в нем есть!')
    await send_text(message, 'Я иногда задумываюсь и могу не ответить сразу. Если ты отправил(-а) мне сообщение, а я ничего не ответил, то отправь это же сообщение мне ещё раз, пожалуйста.')
    await send_text(message, 'На каждой из локаций есть уникальное место, достоприпечательность, которую ты также можешь найти и изучить.')
    await send_text(message, 'Как прибудешь на каждую из локаций, то отправь свое местоположение. Для этого есть кнопка ниже *Отправить локацию*. Если её нет, то смотри её рядом со стикерами, значок квадрата с четырмя квадратами внутри')
    await send_text(message, 'Как доберешся - отправь свою локацию с помощью кнопки ниже 👇', markup)


async def help_loc_3(message):
    await send_reply_text(message.chat.id, 'Используй круглый дешифратор из конверта. Нужно чтобы сердечки на обоих кругах совпали и тогда каждая цифра будет обозначать нужную букву', message.message_id)
    await message.edit_reply_markup()


async def help_loc_4(message):
    await send_reply_text(message.chat.id, 'Попробуй прочитать слово так, как бы его стал читать араб 👳', message.message_id)
    await message.edit_reply_markup()


async def help_loc_5(message):
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


async def help_loc_8(call):
    pass


async def send_text(message: types.Message, text: str, reply_markup: types.ReplyKeyboardMarkup=None, parse_mode: types.ParseMode='markdown') -> types.Message:
    """Отправляем текстовое сообщение в ответ"""
    await message.answer(text=text, reply_markup=reply_markup, parse_mode=parse_mode)


async def send_photo(message: types.Message, img: types.InputMediaPhoto, reply_markup=None) -> types.Message:
    """Отправляем фото"""
    await message.answer_photo(photo=img, reply_markup=reply_markup)


async def send_reply_text(chat_id, text, reply_to_message_id, reply_markup = None, parse_mode = 'markdown'):
    await bot.send_message(chat_id, text, reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, parse_mode=parse_mode)


async def edit_msg(chat_id, msg_id, text, reply_markup = None, parse_mode = 'markdown'):
    await bot.edit_message_text(chat_id=chat_id ,message_id=msg_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

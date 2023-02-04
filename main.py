import database as db
import logging
import os

from aiogram import Bot, Dispatcher, asyncio, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ID_MY = int(os.getenv('MY_ID'))

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[
                        logging.FileHandler(
                            filename='bot_log.log', mode='w', encoding='UTF-8')
                        ])

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    """Класс для сообщения, которое нужно переслать разработчику"""
    answer = State()


# Reply Keyboard для отправки локации
markup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False
)
location = types.KeyboardButton("Отправить локацию", request_location=True)
markup.add(location)

# Убрать Reply Keyboard
hide_kb = types.ReplyKeyboardRemove()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message) -> types.Message:
    """Приветствие"""
    await message.reply(
        text=f'Привет {message.chat.username}! '
        'Нужно кодовое слово, чтобы начать'
    )


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message) -> types.Message:
    """Помощь"""
    await Form.answer.set()
    key_help = types.InlineKeyboardButton(
        text='Отмена', callback_data='cancel'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await send_reply_text(
        message.chat.id, 'Следующуее сообщение я отправлю разработчку',
        message.message_id, kb
    )


@dp.message_handler(state=Form.answer)
async def forward_answer(
    message: types.Message, state: FSMContext
) -> types.Message:
    """Ловим сообщение пользователя после help"""
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
    await bot.send_message(
        message.reply_to_message.chat.id, message.text,
        reply_to_message_id=message.reply_to_message.message_id
    )


@dp.message_handler(content_types=['text'])
async def get_text(message: types.Message) -> None:
    """Получаем текст из сообщения и передаем дальше"""
    text = message.text.lower()
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 f'send text "{text}"')
    if text == 'биоматериал':
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
    await message.answer_sticker(message.sticker.file_id)


@dp.callback_query_handler(
    lambda call: call.data == 'cancel', state=Form.answer
)
async def cancel_callback(
    call: types.CallbackQuery, state: FSMContext
) -> None:
    """Отменяет написание сообщения разработчику"""
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
    elif 59.9642 <= lat <= 59.9647 and 30.3108 <= lon <= 30.3118:
        await location_nine(message)
    else:
        logging.info(f'User {message.chat.id}, {message.chat.username}'
                     f' lat = {lat}, long = {lon}')
        await send_text(message, text='Не похоже что ты на месте')


async def location_one(message: types.Message) -> None:
    """Локация 1"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 1')
    await send_text(
        message, 'Приветствую на первой локации! Это двор Нельсона, '
        'неформальная достопримечательность Петроградской стороны'
    )
    await send_text(
        message, 'И вернемся к делу. Несколько дней назад нам удалось '
        'перехватить сообщение _Мистера Х_:\n\n*Одна из подсказок находится по'
        ' адресу Пионерская улица 22*'
    )
    await send_photo(
        message, 'https://img.the-village.ru/4kNSEWjYk4QPhPSdbGveLGPr8CnK3wje'
        '2OCy3QrTM1Y/rs:fill:620:415/q:88/plain/post-image_featured/Dlk8pFHJK'
        'aVBTf3rd8VNrw.png'
    )
    await send_text(
        message, 'И как прибудешь на локацию - отправь свое местоположение с '
        'помощью кнопки ниже 👇', markup
    )


async def location_two(message: types.Message) -> None:
    """Локация 2"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 2')
    await send_text(
        message, 'Здесь можно найти замечательное граффити "Покорение неба и '
        'космоса"'
    )
    await send_text(
        message, 'Также по этой геоточке есть следующая информация:\n\nСлово '
        'для шифра: *"Датчик"*\n\nДальше следуй во двор по адресу: _Малый '
        'проспект П.С. 1Б_'
    )
    await send_photo(
        message, 'http://risovach.ru/upload/2020/07/mem/hochu-obnimashek_2443'
        '97878_orig_.jpg'
    )
    await send_text(
        message, 'Как прибудешь на локацию - отправь свое местоположение с '
        'помощью кнопки ниже 👇', markup
    )


async def location_three(message: types.Message) -> None:
    """Локация 3"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 3')
    await send_text(message, 'Добро пожаловать в восьмиугольный двор колодец!')
    await send_text(
        message, 'Идём по пятам _Мистера Х_, вот что у нас есть:\n*5 4 30 25 '
        '10 4\n 15 14 10 25 10\n33 1 15 14 1 22 24 1 23 15 35*\n\nИ вот ещё:'
    )
    await send_text(message, '*59.955998, 30.298809*')
    await send_photo(
        message, 'https://lh3.googleusercontent.com/proxy/raysuDMEM2Tpy7JR90E'
        'qf0IGP5St_mOl3G5AlFQEOlfXNllNx9JuCrMa4TEJPmcdWR7-YRzWnccWSUJrZS-EKZa'
        'TMDo'
    )
    key_help = types.InlineKeyboardButton(
        text='Помощь', callback_data='help_loc_3'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await asyncio.sleep(7)
    await edit_reply_markup(message.chat.id, message.message_id + 2, kb)


async def location_four(message: types.Message) -> None:
    """Локация 4"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 4')
    await send_text(
        message, 'На углу дома 10 по Большой Пушкарской можно найти памятную '
        'табличку с тем, какой уровень воды был в городе в 1924 году'
    )
    await send_text(
        message, 'Мы только что перехватили сообщение, может быть это локация '
        '🤔🤔🤔:\n\n*яоцароткивревкс*'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/avajjz44qfu0bdk/%D0%BF%D0%B8%D0%'
        'BA%D0%B0%D1%87%D1%83.jpg'
    )
    await asyncio.sleep(30)
    key_help = types.InlineKeyboardButton(
        text='Помощь', callback_data='help_loc_4'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await edit_reply_markup(message.chat.id, message.message_id + 2, kb)


async def location_five(message: types.Message) -> None:
    """Локация 5"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 5')
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
    await send_text(message, 'Второе ключевое слово: *ПБЩЬДЧ*')
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
    key_help = types.InlineKeyboardButton(
        text='Помощь', callback_data='help_loc_5'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await edit_reply_markup(message.chat.id, message.message_id + 3, kb)


async def location_six(message: types.Message) -> None:
    """Локация 6"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 6')
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


async def location_seven(message: types.Message, second: bool = False) -> None:
    """Локация 7"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 7')
    if not second:
        await send_text(
            message, 'Правильно! Это и есть та точка! Это постройка 1953 г. о '
            'чем свидетельствует дата на фронтоне.'
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
    buttons = []
    for data, text in k.items():
        buttons.extend([types.InlineKeyboardButton(
            text=text, callback_data=data
        )])
    kb = types.InlineKeyboardMarkup()
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
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 8')
    await send_text(
        message, 'Дом Бенуа (также назвают Дом трёх Бенуа) — памятник истории '
        'и культуры регионального значения. Этот доходный дом был построен по '
        'заказу Первого Российского страхового общества в стиле '
        'неоклассицизма по проекту Л. Н. Бенуа, Ю. Ю. Бенуа и А. Н. Бенуа '
        'при участии А. И. Гунста. \nКоличество квартир при постройке дома —'
        ' 250, количество пронумерованных парадных — 25, количество дворов — '
        '12.\nВ Доме Бенуа жило множество знаменитостей. Здесь творили '
        'композиторы Д. Шостакович и Д. Толстой; художники К. Маковский, Л. '
        'Сергеева, А. Мыльников; писатели М. Чехов, В Дорошевич, А. Прокофьев.'
        ' Благодаря своей уникальной архитектуре с множеством дворов здесь '
        'снималось и снимаются фильмы и сериалы. Например "Бандитский '
        'Петербург" или "Улицы разбитых фонарей". Достаточно перейти в '
        'соседний двор и вот уже другая локация в фильме! Также тут снимался '
        'клип группы ДДТ на песню "Одноразовая жизнь".', hide_kb
    )
    await asyncio.sleep(5)
    await send_text(message, 'Продолжим')
    await send_photo(
        message, 'https://www.dropbox.com/s/9zeuqf163j43l7y/%D0%A0%D0%98%D0%'
        '90%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8.jpg'
    )
    await send_text(
        message, 'Где-то в этой новости зашифровано третье ключевое слово, '
        'постарайся вычислить'
    )
    await asyncio.sleep(10)
    await send_text(
        message, 'Пришли нам пожалуйста кодовую фразу из трех слов, которая у '
        'тебя получилась'
    )
    await asyncio.sleep(40)
    key_help = types.InlineKeyboardButton(
        text='Помощь', callback_data='help_loc_8'
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(key_help)
    await edit_reply_markup(message.chat.id, message.message_id+3, kb)


async def location_nine(message: types.Message) -> None:
    """Локация 9"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 9')
    await send_text(
        message, 'Это служебный флигель и скульптурная мастерская постройки '
        '1886 года, отличающаяся от всех зданий вокруг своей высотой.'
    )
    k = {'tamila': 'Тамила', 'jhon': 'Джон', 'bill': 'Билл', 'kevin': 'Кевин'}
    buttons = []
    for data, text in k.items():
        buttons.extend([types.InlineKeyboardButton(
            text=text, callback_data=data
        )])
    kb = types.InlineKeyboardMarkup()
    kb.add(*buttons)
    await send_text(
        message, 'Итак, последняя задачка:\n'
        'Один из частных детективов, который помогал '
        'нам в поисках Мистера Х пропал. Мы уверены, что это связано с его '
        'деятельностью. Мы приехали к нему, чтобы узнать новые детали '
        'поисков, но нашли только хаос и беспорядок в кабинете детектива, '
        'как будто что-то искали и не могли найти. На рабочем месте '
        'нашего знакомого, которое как мы предполагаем посетил Мистер Х, '
        'мы нашли 4 цифры, но что это могло бы значить, мы не знаем. '
        'Думаем, что это какая-то подсказка, которая поможет нам узнать '
        'кто же есть такой этот Мистер Х. И у нас есть четверо '
        'подозреваемых: Тамила (изящная карманниица, пытаемся её поймать, '
        'но все время не хватает улик), Джон (умеет вскрывать любые '
        'замки, давно ничего не было слышно о нем), Билл (недавно приехал'
        ' к нам в город, раньше был замечен за хорошо продуманными планами) '
        'и местный Кевин (маленький вор)', kb
    )


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
        'и решить последнюю задачку, она тут недалеко. Хочешь?', kb
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
        message, 'Хорошо! Тогда следуй на Большой проспек П.С. 71 лит Б',
        markup
    )


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


async def edit_reply_markup(
    chat_id: int, msg_id: int, reply_markup: types.ReplyKeyboardMarkup
) -> types.Message:
    """Добавляем Inline keyboard"""
    await bot.edit_message_reply_markup(
        chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

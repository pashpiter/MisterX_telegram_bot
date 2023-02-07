from aiogram import asyncio, types

from bot_settings import logging
from markups import edit_reply_markup, hide_kb, markup
from send_msg import send_photo, send_text


async def location_one(message: types.Message) -> None:
    """Локация 1"""
    logging.info(f'User {message.chat.id}, {message.chat.username} '
                 'location 1')
    await send_text(
        message, 'Приветствую на первой локации! Это двор Нельсона, '
        'неформальная достопримечательность Петроградской стороны.\n'
        'Здесь можно найти удивительные улично-дворовые арт-объекты и '
        'красочные произведения искусства, а все это - творения рук здешнего'
        ' барда Нельсона. Можно пройтись, обратить внимание на стены, '
        'заглянуть в арки, и возможно даже встретить создателя.'
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
        '10 4\n15 14 10 25 10\n33 1 15 14 1 22 24 1 23 15 35*\n\nИ вот ещё:'
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
        'животных.\nЭто один из северных зоопарков мира, где содеражтся около '
        '600 видов млекопитающих, птиц, рыб и беспозвоночных из разных уголков'
        ' Земли.'
    )
    await send_text(
        message, 'Итак, вернемся к поиску. У тебя уже есть шифр с квадратами, '
        'расставь на нем фигуры так, чтобы в каждом столбце, строке и в каждом'
        ' квадрате с двойной границей были разные фигуры, как в *судоку*, '
        'только с фигурами. Острие треугольников должны смотреть вверх. Затем '
        'сопоставь судоку с картинкой и треугольники подскажут тебе следующее '
        'место, на Петроградской стороне, куда тебе нужно добраться.'
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
    kb = types.InlineKeyboardMarkup(row_width=2)
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
        'и местный Кевин (маленький вор)'
    )
    await send_photo(
        message, 'https://www.dropbox.com/s/0rfay2izcc3uaei/d2aebd560cbed117db'
        'a06686b8.jpg', kb
    )

from aiogram import types


async def log_answer(message: types.Message, key: str) -> types.Message:
    """Присылает последние логи программы"""
    k = {
        'log_5': 5, 'log_10': 10, 'log_15': 15,
        'log_20': 20, 'log_25': 25, 'log_30': 30
    }
    f = open('bot_log.log', encoding='UTF-8')
    text = [line for line in f]
    f.close()
    await message.reply(''.join(text[-k[key]:]))
    await message.edit_reply_markup()

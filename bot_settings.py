import json
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
ID_MY = int(os.getenv('MY_ID'))
CODE_WORDS = json.loads(os.environ['CODE_WORDS'])

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(
                            filename='bot_log.log', mode='w', encoding='UTF-8')
                        ])

import logging
from dataclasses import dataclass
from utils.api_service import APIService
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from db_handler.db_sqlite import DBSqlite
from decouple import config
from states.state_manager import StateManager

db = DBSqlite()
api_service = APIService(db)
state_manager = StateManager()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
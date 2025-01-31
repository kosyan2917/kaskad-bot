from abc import ABC, abstractmethod
from aiogram.types import Message

class State:
    @abstractmethod
    async def on_enter(self, message: Message) -> None:
        pass
from aiogram import BaseMiddleware
from aiogram.types import Message
from create_bot import state_manager, db
from typing import Awaitable, Callable

class StateMiddleware(BaseMiddleware):
    pass

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, any]], Awaitable[any]],
        event: Message,
        data: dict[str, any]
    ) -> any:
        user = event.from_user.id
        if not user in state_manager.get_states():
            if db.check_user(user):
                await state_manager.set_state(user, state_manager.main, event)
            else:
                await state_manager.set_state(user, state_manager.unauthorized, event)
        return await handler(event, data)

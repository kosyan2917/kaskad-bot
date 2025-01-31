from states.states_interface import State
from aiogram.types import Message

class StateManager:
    def __init__(self):
        self.__states = {}

    async def set_state(self, user: str, state: State, message: Message) -> None:
        self.__states[user] = state
        print(self.__states)
        await state.on_enter(message)

    def get_states(self) -> None:
        return self.__states
    
    def get_user_state(self, user: str) -> State:
        return self.__states[user]

    @classmethod
    def register_state(cls, state: State) -> None:
        if isinstance(state, State):
            if state.__class__.__name__.lower().endswith("state"):
                name = state.__class__.__name__.lower()[:-5]
            else:
                name = state.__class__.__name__.lower()
            setattr(cls, name, state)
        else:
            raise NotImplementedError
            
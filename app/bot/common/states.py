from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    language = State()
    username = State()
    fio = State()
    phone = State()
    documents = State()
    instructions = State()
    verification = State()
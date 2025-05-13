from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    language = State()
    username = State()
    fio = State()
    phone = State()
    documents = State()
    instructions = State()
    verification = State()

class NotifyObjectStates(StatesGroup):
    waiting_message = State()

class ObjectPhotoStates(StatesGroup):
    waiting_photo = State()
    waiting_description = State()

class ObjectCheckStates(StatesGroup):
    waiting_photo = State()
    waiting_description = State()
    waiting_amount = State()
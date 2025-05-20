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
    waiting_photo_and_desription = State()
    waiting_amount = State()

class MaterialRemainderStates(StatesGroup):
    waiting_photo = State()
    waiting_description = State()
    waiting_location = State()

class MaterialOrderStates(StatesGroup):
    waiting_description = State()
    waiting_date = State()

class HandoverStates(StatesGroup):
    waiting_description = State()
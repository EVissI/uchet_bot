from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

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

class ExportXlsxStates(StatesGroup):
    waiting_start_date = State()
    waiting_end_date = State()
    waiting_expense_type = State()

class AdminPanelStates(StatesGroup):
    objects_control = State()
    tools_control = State()
    material_remainder_control = State()
    material_remainder_change_deactivate = State()

class CreateObjectStates(StatesGroup):
    waiting_name = State()
    waiting_description = State()
    waiting_documents = State()

class AdminAddMemberToObjectStates(StatesGroup):
    waiting_user_ids = State()

class AdminNotify(StatesGroup):
    waiting_message = State()
    waiting_object_message = State()

class BulkTransferStates(StatesGroup):
    waiting_file = State()

class TMCStates(StatesGroup):
    input_name = State()
    input_description = State()
    input_file = State()
    input_quantity = State()

class AdminCheckStates(StatesGroup):
    waiting_photo_and_description = State()
    waiting_amount = State()
    confirm_send_to_group = State()

class CheckOutObjectStates(StatesGroup):
    waiting_photo = State()
    waiting_amount = State()

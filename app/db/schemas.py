from pydantic import BaseModel

class TelegramIDModel(BaseModel):
    telegram_id: int
    class Config:
        from_attributes = True

class UserModel(TelegramIDModel):
    username: str 
    phone_number: str 
    user_enter_fio: str 
    role: str 
    can_use_bot: bool 
    last_message_id: int

class UserFilterModel(BaseModel):
    telegram_id: int | None = None
    username: str | None = None
    phone_number: str | None = None
    user_enter_fio: str | None = None
    role: str | None = None
    can_use_bot: bool | None = None
    last_message_id: int | None = None

class UserDocumentModel(BaseModel):
    file_id:int
    user_id:int
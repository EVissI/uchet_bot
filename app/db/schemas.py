from pydantic import BaseModel

class TelegramIDModel(BaseModel):
    telegram_id: int
    class Config:
        from_attributes = True

class UserModel(TelegramIDModel):
    username: str 
    language: str
    phone_number: str 
    user_enter_fio: str 
    role: str 
    can_use_bot: bool 

class UserFilterModel(BaseModel):
    telegram_id: int | None = None
    username: str | None = None
    language: str | None = None
    phone_number: str | None = None
    user_enter_fio: str | None = None
    role: str | None = None
    can_use_bot: bool | None = None

class UserDocumentModel(BaseModel):
    file_id:int
    user_id:int

class ToolModel(BaseModel):
    name: str
    description: str | None = None
    file_id: str | None = None
    user_id: int

    class Config:
        from_attributes = True

class ToolFilterModel(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    file_id: str | None = None
    user_id: int | None = None
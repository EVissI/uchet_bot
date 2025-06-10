from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import JSON
from app.db.models import ObjectDocument
from app.db.models import Tool


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
    telegram_id: Optional[int] = None
    username: Optional[str] = None
    language: Optional[str] = None
    phone_number: Optional[str] = None
    user_enter_fio: Optional[str] = None
    role: Optional[str] = None
    can_use_bot: Optional[bool] = None


class UserDocumentModel(BaseModel):
    file_id: str
    user_id: int


class ToolModel(BaseModel):
    name: str
    description: Optional[str] = None
    file_id: Optional[str] = None
    status: str
    user_id: int

    class Config:
        from_attributes = True


class ToolFilterModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    file_id: Optional[str] = None
    user_id: Optional[int] = None


class ObjectModel(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    creator_id: int

    class Config:
        from_attributes = True


class ObjectFilterModel(BaseModel):
    id: Optional[int] = None

    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    creator_id: Optional[int] = None


class ObjectDocumentModel(BaseModel):
    object_id: int
    file_id: str
    document_type: str

    class Config:
        from_attributes = True


class ObjectDocumentFilterModel(BaseModel):
    id: Optional[int] = None

    object_id: Optional[int] = None
    file_id: Optional[str] = None
    document_type: Optional[str] = None


class ObjectMemberModel(BaseModel):
    object_id: int
    user_id: int

    class Config:
        from_attributes = True


class CheclModel(BaseModel):
    file_id: str
    amount: float
    description: str
    own_expense: bool = False

    user_id: int

    class Config:
        from_attributes = True


class CheckFilterModel(BaseModel):
    id: Optional[int] = None

    file_id: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    own_expense: Optional[bool] = None

    user_id: Optional[int] = None


class ObjectMemberFilterModel(BaseModel):
    id: Optional[int] = None

    object_id: Optional[int] = None
    user_id: Optional[int] = None


class ObjectCheckModel(BaseModel):
    file_id: str
    amount: float
    description: Optional[str]
    own_expense: bool = False

    object_id: int
    user_id: int

    class Config:
        from_attributes = True


class ObjectCheckFilterModel(BaseModel):
    id: Optional[int] = None

    file_id: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    own_expense: Optional[bool] = None

    object_id: Optional[int] = None
    user_id: Optional[int] = None


class ObjectPhotoModel(BaseModel):
    file_id: str
    description: Optional[str] = None
    object_id: int
    user_id: int

    class Config:
        from_attributes = True


class ObjectPhotoFilterModel(BaseModel):
    id: Optional[int] = None
    file_id: Optional[str] = None
    description: Optional[str] = None
    object_id: Optional[int] = None
    user_id: Optional[int] = None


class NotificationFilter(BaseModel):
    message: Optional[str] = None
    first_notification_time: Optional[datetime] = None
    second_notification_time: Optional[datetime] = None


class MaterialReminderModel(BaseModel):
    description: str
    file_id: str
    storage_location: str
    message_id: Optional[int] = None
    is_active:bool

    class Config:
        from_attributes = True


class MaterialReminderFilter(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    file_id: Optional[str] = None
    storage_location: Optional[str] = None
    message_id: Optional[int] = None
    is_active:bool = None


class MaterialOrderModel(BaseModel):
    description: str
    delivery_date: str
    message_id: Optional[int] = None

    class Config:
        from_attributes = True


class MaterialOrderFilter(BaseModel):
    id: Optional[int] = None
    message_id: Optional[int] = None


class CheckModel(BaseModel):
    file_id: str
    amount: float
    description: Optional[str] = None
    own_expense: bool = False

    user_id: int

    class Config:
        from_attributes = True


class CheckFilterModel(BaseModel):
    id: Optional[int] = None
    file_id: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    own_expense: Optional[bool] = None

    user_id: Optional[int] = None


class ProficAccountingModel(BaseModel):
    object_id: int
    amount: float
    purpose: str
    payment_type: str  # "приход" or "расход"
    created_by: int

    class Config:
        from_attributes = True


class ProficAccountingFilterModel(BaseModel):
    id: Optional[int] = None
    object_id: Optional[int] = None
    amount: Optional[float] = None
    purpose: Optional[str] = None
    payment_type: Optional[str] = None
    created_by: Optional[int] = None

class AdminUserModel(BaseModel):
    username:str
    password:str

class AdminUserFilter(BaseModel):
    username:str = None
    password:str = None
    last_login:datetime = None

class AdminActionLogModel(BaseModel):
    admin_user_id:int
    action:str
    model:str
    record_id:int 
    details:JSON  
    model_config = {
        "arbitrary_types_allowed": True,
        "from_attributes": True
    }

class AdminActionLogModel(BaseModel):
    admin_user_id:int = None
    action:str = None
    model:str = None
    record_id:int = None 
    details:JSON = None  
    model_config = {
        "arbitrary_types_allowed": True,
        "from_attributes": True
    }
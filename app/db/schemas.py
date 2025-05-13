from pydantic import BaseModel
from typing import Optional
from app.db.models import ObjectDocument

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
    file_id:int
    user_id:int

class ToolModel(BaseModel):
    name: str
    description: Optional[str] = None
    file_id: Optional[str] = None
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
    invite_link: Optional[str] = None
    is_active: bool = True
    creator_id: int

    class Config:
        from_attributes = True

class ObjectFilterModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    is_active: Optional[bool] = None
    creator_id: Optional[int] = None

class ObjectDocumentModel(BaseModel):
    object_id: int
    file_id: str
    document_type: ObjectDocument.DocumentType

    class Config:
        from_attributes = True

class ObjectDocumentFilterModel(BaseModel):
    id: Optional[int] = None
    object_id: Optional[int] = None
    file_id: Optional[str] = None
    document_type: Optional[ObjectDocument.DocumentType] = None

class ObjectMemberModel(BaseModel):
    object_id: int
    user_id: int

    class Config:
        from_attributes = True

class ObjectMemberFilterModel(BaseModel):
    id: Optional[int] = None
    object_id: Optional[int] = None
    user_id: Optional[int] = None

class ObjectCheckModel(BaseModel):
    file_id: str
    amount: float
    description:str
    object_id: int
    user_id: int

    class Config:
        from_attributes = True

class ObjectCheckFilterModel(BaseModel):
    id: Optional[int] = None
    file_id: Optional[str] = None
    amount: Optional[float] = None
    description:Optional[str] = None
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
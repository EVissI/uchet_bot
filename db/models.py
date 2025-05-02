from datetime import datetime
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    JSON,
    BigInteger,
    Column,
    DateTime,
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from typing import Optional
from db.database import Base


class User(Base):
    __tablename__ = "users"

    class Role(enum.Enum):
        admin = "администратор"
        worker = "рабочий"
        foreman = "бригадир"
        buyer = "закупщик"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="ru")
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    user_enter_fio: Mapped[str] = mapped_column(String(60), nullable=False)
    last_message_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True, default=None
    )
    role: Mapped[Role] = mapped_column(String(20), nullable=False, default=Role.worker)
    can_use_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    documents:Mapped['UserDocument'] = relationship("UserDocument", back_populates="user", cascade="all, delete")
    objects:Mapped['ObjectMember'] = relationship("ObjectMember", back_populates="user")

class UserDocument(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    
    user:Mapped['User'] = relationship("User", back_populates="documents")

class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    invite_link: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))

    documents:Mapped['ObjectDocument'] = relationship("ObjectDocument", back_populates="object", cascade="all, delete")
    members:Mapped['ObjectMember'] = relationship("ObjectMember", back_populates="object", cascade="all, delete")
    creator:Mapped['User'] = relationship("User", foreign_keys=[creator_id])

class ObjectDocument(Base):
    __tablename__ = "object_documents"

    class DocumentType(enum.Enum):
        estimate = "смета"
        technical_task = "техническое задание"
        customer_contacts = "контакты заказчика"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    document_type: Mapped[DocumentType] = mapped_column(String(20), nullable=False)
    
    object:Mapped['Object'] = relationship("Object", back_populates="documents")

class ObjectMember(Base):
    __tablename__ = "object_members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    
    object: Mapped['Object'] = relationship("Object", back_populates="members")
    user: Mapped['User'] = relationship("User", back_populates="objects")

class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=True)
    storage_location: Mapped[str] = mapped_column(String(255), nullable=True)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
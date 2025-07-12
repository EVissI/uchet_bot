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
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    class Role(enum.Enum):
        admin = "администратор"
        worker = "рабочий"
        foreman = "бригадир"
        buyer = "закупщик"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="ru")
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    user_enter_fio: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[Role] = mapped_column(String(20), nullable=False, default=Role.worker)
    can_use_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    objects: Mapped[list["Object"]] = relationship(
        "Object",
        secondary="object_members",
        primaryjoin="User.telegram_id == ObjectMember.user_id",
        secondaryjoin="ObjectMember.object_id == Object.id",
        back_populates="members",
        viewonly=True
    )

    object_members: Mapped[list["ObjectMember"]] = relationship(
        "ObjectMember", 
        back_populates="user",
        cascade="all, delete"
    )
    tools: Mapped[list["Tool"]] = relationship("Tool", back_populates="user")
    checks: Mapped[list["Check"]] = relationship("Check", back_populates="user")
    object_checks: Mapped[list["ObjectCheck"]] = relationship(
        "ObjectCheck", back_populates="user"
    )
    object_photos: Mapped[list["ObjectPhoto"]] = relationship(
        "ObjectPhoto", back_populates="user"
    )
    documents: Mapped[list["UserDocument"]] = relationship(
        "UserDocument", back_populates="user"
    )
    object_profic_accounting: Mapped[list["ObjectProficAccounting"]] = relationship(
        "ObjectProficAccounting", back_populates="user"
    )
    profic_accounting: Mapped[list["ProficAccounting"]] = relationship(
        "ProficAccounting", back_populates="user"
    )


class Tool(Base):
    __tablename__ = "tools"

    class Status(enum.Enum):
        free = "свободный"
        in_work = "занят"
        repair = "в ремонте"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=True
    )
    status: Mapped[Status] = mapped_column(
        String(20), nullable=False, default=Status.free
    )

    user: Mapped["User"] = relationship("User", back_populates="tools")


class UserDocument(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="documents")


class Object(Base):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    documents: Mapped[list["ObjectDocument"]] = relationship(
        "ObjectDocument", back_populates="object", cascade="all, delete"
    )
    members: Mapped[list["User"]] = relationship(
        "User",
        secondary="object_members",
        primaryjoin="Object.id == ObjectMember.object_id",
        secondaryjoin="ObjectMember.user_id == User.telegram_id",
        back_populates="objects",
        viewonly=True
    )
    object_members: Mapped[list["ObjectMember"]] = relationship(
        "ObjectMember", 
        back_populates="object",
        cascade="all, delete"
    )
    object_checks: Mapped[list["ObjectCheck"]] = relationship(
        "ObjectCheck", back_populates="object", cascade="all, delete"
    )
    photos: Mapped[list["ObjectPhoto"]] = relationship(
        "ObjectPhoto", back_populates="object", cascade="all, delete"
    )
    object_profic_accounting: Mapped[list["ObjectProficAccounting"]] = relationship(
        "ObjectProficAccounting", back_populates="object", cascade="all, delete"
    )
    material_orders: Mapped[list["ObjectMaterialOrder"]] = relationship(
        "ObjectMaterialOrder", back_populates="object", cascade="all, delete"
    )
    

class ObjectPhoto(Base):
    __tablename__ = "object_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    object_id: Mapped[int] = mapped_column(
        ForeignKey("objects.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="object_photos")
    object: Mapped["Object"] = relationship("Object", back_populates="photos")


class ObjectDocument(Base):
    __tablename__ = "object_documents"

    class DocumentFileType(enum.Enum):
        photo = "фото"
        pdf = "pdf"


    class DocumentType(enum.Enum):
        estimate = "смета"
        technical_task = "техническое задание"
        customer_contacts = "контакты заказчика"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    document_type: Mapped[DocumentType] = mapped_column(String(20), nullable=False)
    document_file_type: Mapped[DocumentFileType] = mapped_column(
        String(20), nullable=False, default=DocumentFileType.pdf
    )

    object: Mapped["Object"] = relationship("Object", back_populates="documents")


class ObjectMember(Base):
    __tablename__ = "object_members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(ForeignKey("objects.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE")
    )

    object: Mapped["Object"] = relationship("Object", back_populates="object_members")
    user: Mapped["User"] = relationship("User", back_populates="object_members")



class MaterialReminder(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=True)
    storage_location: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    own_expense: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="checks")


class ObjectCheck(Base):
    __tablename__ = "object_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    own_expense: Mapped[bool] = mapped_column(Boolean, default=False)

    object_id: Mapped[int] = mapped_column(
        ForeignKey("objects.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="object_checks")
    object: Mapped["Object"] = relationship("Object", back_populates="object_checks")


class WorkerNotification(Base):
    __tablename__ = "worker_notification"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    message: Mapped[str]
    first_notification_time: Mapped[datetime]
    second_notification_time: Mapped[datetime]


class ForemanNotification(Base):
    __tablename__ = "foreman_notification"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    message: Mapped[str]
    first_notification_time: Mapped[datetime]
    second_notification_time: Mapped[datetime]


class MaterialOrder(Base):
    __tablename__ = "material_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    delivery_date: Mapped[str] = mapped_column(String(20), nullable=False)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ObjectMaterialOrder(Base):
    __tablename__ = "object_material_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    delivery_date: Mapped[str] = mapped_column(String(20), nullable=False)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    object_id: Mapped[int] = mapped_column(
        ForeignKey("objects.id", ondelete="CASCADE"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    object: Mapped["Object"] = relationship("Object", back_populates="material_orders")

class ObjectProficAccounting(Base):
    __tablename__ = "object_profic_accounting"

    class PaymentType(enum.Enum):
        income = "приход"
        expense = "расход"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(
        ForeignKey("objects.id", ondelete="CASCADE"), nullable=False
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(String(20), nullable=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    object: Mapped["Object"] = relationship(
        "Object", back_populates="object_profic_accounting"
    )
    user: Mapped["User"] = relationship("User", back_populates="object_profic_accounting")

class ProficAccounting(Base):
    __tablename__ = "profic_accounting"

    class PaymentType(enum.Enum):
        income = "приход"
        expense = "расход"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(String(20), nullable=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="profic_accounting")


class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    last_login = Column(DateTime(timezone=True))

    action_logs = relationship("AdminActionLog", back_populates="admin_user")

class AdminActionLog(Base):
    __tablename__ = 'admin_action_logs'

    id = Column(Integer, primary_key=True)
    admin_user_id = Column(Integer, ForeignKey('admin_users.id'))
    action = Column(String(50))  
    model = Column(String(50))   
    record_id = Column(BigInteger)  
    details = Column(JSON)       

    admin_user = relationship("AdminUser", back_populates="action_logs")
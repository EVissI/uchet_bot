from loguru import logger
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.db.base import BaseDAO
from app.db.models import (
    User,
    UserDocument,
    Tool,
    Object,
    ObjectDocument,
    ObjectMember,
    MaterialReminder,
    Check,
    ObjectCheck,
    ObjectPhoto,
    WorkerNotification,
    ForemanNotification,
    MaterialOrder,
    ObjectProficAccounting,
    ProficAccounting
)

from app.db.schemas import MaterialReminderFilter, TelegramIDModel, UserFilterModel


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_all_except(
        cls, session: AsyncSession, exclude_user_id: int
    ) -> list[User]:
        """
        Find all active users except specified user

        Args:
            session: AsyncSession - DB session
            exclude_user_id: int - Telegram ID of user to exclude

        Returns:
            list[User]: List of users excluding specified user
        """
        try:
            stmt = (
                select(cls.model)
                .where(
                    cls.model.telegram_id != exclude_user_id,
                    cls.model.can_use_bot == True,
                )
                .order_by(cls.model.user_enter_fio)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            logger.error(f"Error in find_all_except: {e}")
            return []

    @classmethod
    async def find_by_telegram_id(
        cls, session: AsyncSession, telegram_id: int
    ) -> User | None:
        """
        find user by telegram id
        """
        filters = TelegramIDModel(telegram_id=telegram_id)
        return await UserDAO.find_one_or_none(session, filters=filters)

    @classmethod
    async def find_by_identifier(
        cls, session: AsyncSession, identifier: str
    ) -> User | None:
        """
        Find user by username or telegram_id

        Args:
            session: AsyncSession - DB session
            identifier: str - Username (@username) or Telegram ID

        Returns:
            User | None: Found user or None
        """
        try:
            identifier = identifier.strip("@") if identifier else None
            if not identifier:
                return None

            if identifier.isdigit():
                user = await cls.find_one_or_none(
                    session, UserFilterModel(telegram_id=int(identifier))
                )
                if user:
                    return user

            return await cls.find_one_or_none(
                session, UserFilterModel(username=identifier)
            )

        except SQLAlchemyError as e:
            logger.error(f"Error in find_by_identifier: {e}")
            return None


class UserDocumentDAO(BaseDAO):
    model = UserDocument


class ToolDAO(BaseDAO):
    model = Tool

    @classmethod
    async def get_filtered_tools(cls, session: AsyncSession, status: str) -> list[Tool]:
        """Get filtered tools by status"""
        try:
            conditions = []

            if status == "in_work":
                conditions.append(cls.model.status == Tool.Status.in_work.value)
            if status == "free":
                conditions.append(cls.model.status == Tool.Status.free.value)
            if status == "repair":
                conditions.append(cls.model.status == Tool.Status.repair.value)

            result = await session.execute(
                select(cls.model)
                .where(*conditions)
                .options(joinedload(cls.model.user))
                .order_by(cls.model.created_at)
            )
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            logger.error(f"Error in get_filtered_tools: {e}")
            return []


class ObjectDAO(BaseDAO):
    model = Object


class ObjectDocumentDAO(BaseDAO):
    model = ObjectDocument

    @classmethod
    async def find_object_documents(
        cls, session: AsyncSession, object_id: int, user_role: User.Role
    ) -> list[ObjectDocument]:
        """
        Find all documents attached to a specific object.
        For workers, return only technical_task documents.
        """
        try:
            query = select(cls.model).where(cls.model.object_id == object_id)
            if user_role == User.Role.worker:
                query = query.where(cls.model.document_type == ObjectDocument.DocumentType.technical_task)
            result = await session.execute(query.order_by(cls.model.created_at))
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error in find_object_documents: {e}")
            return []


class ObjectMemberDAO(BaseDAO):
    model = ObjectMember

    async def find_user_objects(session: AsyncSession, user_id: int) -> list[Object]:
        """
        Find all active objects assigned to user
        Args:
            session: AsyncSession
            user_id: Telegram ID of the user
        Returns:
            list[Object]: List of objects assigned to user
        """
        stmt = (
            select(Object)
            .join(ObjectMember, Object.id == ObjectMember.object_id)
            .where(ObjectMember.user_id == user_id, Object.is_active == True)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_object_members(
        cls, session: AsyncSession, object_id: int
    ) -> list[User]:
        """
        Find all unique users assigned to specific object
        Args:
            session: AsyncSession
            object_id: ID of the object
        Returns:
            list[User]: List of unique users assigned to object
        """
        try:
            stmt = (
                select(User)
                .distinct()
                .join(ObjectMember, User.telegram_id == ObjectMember.user_id)
                .where(ObjectMember.object_id == object_id, User.can_use_bot == True)
                .order_by(User.user_enter_fio)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error in find_object_members: {e}")
            return []

    @classmethod
    async def find_object_members_except(
        cls, session: AsyncSession, object_id: int, exclude_user_id: int
    ) -> list[User]:
        """
        Find all unique users assigned to specific object except specified user

        Args:
            session: AsyncSession - DB session
            object_id: ID of the object
            exclude_user_id: Telegram ID of user to exclude

        Returns:
            list[User]: List of unique users assigned to object (excluding specified user)
        """
        try:
            stmt = (
                select(User)
                .distinct()
                .join(ObjectMember, User.telegram_id == ObjectMember.user_id)
                .where(
                    ObjectMember.object_id == object_id,
                    User.can_use_bot == True,
                    User.telegram_id != exclude_user_id,
                )
                .order_by(User.user_enter_fio)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error in find_object_members_except: {e}")
            return []


class MaterialReminderDAO(BaseDAO):
    model = MaterialReminder

    @classmethod
    async def find_material_reminder_by_page(
        cls, session: AsyncSession, page: int
    ) -> tuple[int, int, int] | None:
        """
        retun page, total reminders count, id of reminder on that page
        """
        reminders: list[MaterialReminder] = await MaterialReminderDAO.find_all(
            session, MaterialReminderFilter()
        )
        if reminders:
            return (page, len(reminders), reminders[page - 1].id)


class CheckDAO(BaseDAO):
    model = Check

    @staticmethod
    async def get_by_date_range(
        session: AsyncSession, start_date: datetime, end_date: datetime
    ) -> list[Check]:
        query = (
            select(Check)
            .where(and_(Check.created_at >= start_date, Check.created_at <= end_date))
            .options(joinedload(Check.user))
            .order_by(Check.created_at)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    def serialize_for_report(record: Check) -> dict:
        return {
            "created_at": record.created_at,
            "amount": getattr(record, "amount", None),
            "description": getattr(record, "description", None),
            "own_expense": getattr(record, "own_expense", None),
            "user_fio": (
                getattr(record.user, "user_enter_fio", None)
                if hasattr(record, "user")
                else None
            ),
        }


class ObjectCheckDAO(BaseDAO):
    model = ObjectCheck

    @classmethod
    async def get_filtered_expenses(
        cls,
        session: AsyncSession,
        object_id: int,
        start_date: datetime,
        end_date: datetime,
        expense_type: str,
    ) -> list[ObjectCheck]:
        """
        Get filtered expenses for an object within a date range and by type.

        Args:
            session: AsyncSession - DB session
            object_id: int - ID of the object
            start_date: datetime - Start date of the period
            end_date: datetime - End date of the period
            expense_type: str - Type of expenses ('all', 'own', 'company')

        Returns:
            list[ObjectCheck]: List of filtered expenses
        """
        try:
            conditions = [
                cls.model.object_id == object_id,
                cls.model.created_at >= start_date,
                cls.model.created_at <= end_date,
            ]

            # Add expense type filter if not 'all'
            if expense_type == "own":
                conditions.append(cls.model.own_expense == True)
            elif expense_type == "company":
                conditions.append(cls.model.own_expense == False)

            result = await session.execute(
                select(cls.model)
                .where(*conditions)
                .order_by(cls.model.created_at)
                .options(joinedload(cls.model.user))
            )
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            logger.error(f"Error in get_filtered_expenses: {e}")
            return []

    @staticmethod
    async def get_by_date_range(
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        object_id: int | None = None,
    ) -> list[ObjectCheck]:
        """Get object checks by date range and optionally by object"""
        query = (
            select(ObjectCheck)
            .where(
                and_(
                    ObjectCheck.created_at >= start_date,
                    ObjectCheck.created_at <= end_date,
                )
            )
            .options(joinedload(ObjectCheck.user), joinedload(ObjectCheck.object))
        )
        if object_id is not None:
            query = query.where(ObjectCheck.object_id == object_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    def serialize_for_report(record: ObjectCheck) -> dict:
        return {
            "created_at": record.created_at,
            "amount": getattr(record, "amount", None),
            "description": getattr(record, "description", None),
            "own_expense": getattr(record, "own_expense", None),
            "object_name": (
                getattr(record.object, "name", None)
                if hasattr(record, "object")
                else None
            ),
            "user_fio": (
                getattr(record.user, "user_enter_fio", None)
                if hasattr(record, "user")
                else None
            ),
        }


class ObjectPhotoDAO(BaseDAO):
    model = ObjectPhoto


class WorkerNotificationDAO(BaseDAO):
    model = WorkerNotification


class ForemanNotificationDAO(BaseDAO):
    model = ForemanNotification


class MaterialOrderDAO(BaseDAO):
    model = MaterialOrder


class ObjectProficAccountingDAO(BaseDAO):
    model = ObjectProficAccounting

    @staticmethod
    async def get_by_date_range(
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        object_id: int | None = None,
    ) -> list[ObjectProficAccounting]:
        """Get profic accounting records by date range and optionally by object"""
        query = (
            select(ObjectProficAccounting)
            .where(
                and_(
                    ObjectProficAccounting.created_at >= start_date,
                    ObjectProficAccounting.created_at <= end_date,
                )
            )
            .options(
                joinedload(ObjectProficAccounting.user), joinedload(ObjectProficAccounting.object)
            )
        )
        if object_id is not None:
            query = query.where(ObjectProficAccounting.object_id == object_id)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    def serialize_for_report(record: ObjectProficAccounting) -> dict:
        return {
            "created_at": record.created_at,
            "payment_type": getattr(record, "payment_type", None),
            "object_name": (
                getattr(record.object, "name", None)
                if hasattr(record, "object")
                else None
            ),
            "purpose": getattr(record, "purpose", None),
            "amount": getattr(record, "amount", None),
            "user_fio": (
                getattr(record.user, "user_enter_fio", None)
                if hasattr(record, "user")
                else None
            ),
        }


class ProficAccountingDAO(BaseDAO):
    model = ProficAccounting

    @staticmethod
    async def get_by_date_range(
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime,
        object_id: int | None = None,
    ) -> list[ProficAccounting]:
        """Get profic accounting records by date range and optionally by object"""
        query = (
            select(ProficAccounting)
            .where(
                and_(
                    ProficAccounting.created_at >= start_date,
                    ProficAccounting.created_at <= end_date,
                )
            )
            .options(
                joinedload(ProficAccounting.user), joinedload(ProficAccounting.object)
            )
        )
        if object_id is not None:
            query = query.where(ProficAccounting.object_id == object_id)
        result = await session.execute(query)
        return result.scalars().all()

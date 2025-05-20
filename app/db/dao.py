from loguru import logger
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseDAO
from app.db.models import (
    User, UserDocument, Tool, Object, 
    ObjectDocument, ObjectMember, Material,
    Check, ObjectCheck, ObjectPhoto,WorkerNotification,ForemanNotification,MaterialOrder
)

from app.db.schemas import TelegramIDModel


class UserDAO(BaseDAO):
    model = User

    async def find_by_telegram_id(session:AsyncSession, telegram_id:int) -> User | None:
        """
        find user by telegram id
        """
        filters = TelegramIDModel(telegram_id=telegram_id)
        return await UserDAO.find_one_or_none(session,filters=filters)
    
class UserDocumentDAO(BaseDAO):
    model = UserDocument

class ToolDAO(BaseDAO):
    model = Tool

class ObjectDAO(BaseDAO):
    model = Object

class ObjectDocumentDAO(BaseDAO):
    model = ObjectDocument
    
    @classmethod
    async def find_object_documents(cls, session: AsyncSession, object_id: int, user_role: User.Role) -> list[ObjectDocument]:
        """
        Find all documents attached to a specific object.
        
        Args:
            session: AsyncSession - DB session
            object_id: int - ID of the object
            user_role: User.Role - Role of user (not used currently)
            
        Returns:
            list[ObjectDocument]: List of documents attached to object
        """
        try:
            result = await session.execute(
                select(cls.model)
                .where(cls.model.object_id == object_id)
                .order_by(cls.model.created_at)
            )
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
            .where(
                ObjectMember.user_id == user_id,
                Object.is_active == True
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    

    async def find_object_members(session: AsyncSession, object_id: int) -> list[User]:
        """
        Find all users assigned to specific object
        Args:
            session: AsyncSession
            object_id: ID of the object
        Returns:
            list[User]: List of users assigned to object
        """
        stmt = (
            select(User)
            .join(ObjectMember, User.telegram_id == ObjectMember.user_id)
            .where(
                ObjectMember.object_id == object_id,
                User.can_use_bot == True
            )
            .order_by(User.user_enter_fio)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    

class MaterialDAO(BaseDAO):
    model = Material

class CheckDAO(BaseDAO):
    model = Check

class ObjectCheckDAO(BaseDAO):
    model = ObjectCheck

class ObjectPhotoDAO(BaseDAO):
    model = ObjectPhoto

class WorkerNotificationDAO(BaseDAO):
    model = WorkerNotification

class ForemanNotificationDAO(BaseDAO):
    model = ForemanNotification

class MaterialOrderDAO(BaseDAO):
    model = MaterialOrder
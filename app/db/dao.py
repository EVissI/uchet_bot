from loguru import logger
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseDAO
from app.db.models import (
    User, UserDocument, Tool, Object, 
    ObjectDocument, ObjectMember, Material,
    Check, ObjectCheck
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

class ObjectMemberDAO(BaseDAO):
    model = ObjectMember

    async def find_user_objects(self, session: AsyncSession, user_id: int) -> list[Object]:
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

class MaterialDAO(BaseDAO):
    model = Material

class CheckDAO(BaseDAO):
    model = Check

class ObjectCheckDAO(BaseDAO):
    model = ObjectCheck
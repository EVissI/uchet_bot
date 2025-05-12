from loguru import logger
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseDAO
from app.db.models import User,UserDocument,Tool
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
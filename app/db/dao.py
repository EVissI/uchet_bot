from loguru import logger
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import BaseDAO
from app.db.models import User,UserDocument


class UserDAO(BaseDAO):
    model = User

class UserDocumentDAO(BaseDAO):
    model = UserDocument
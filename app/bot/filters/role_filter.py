from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from app.db.models import User
from app.db.dao import UserDAO
from app.db.database import async_session_maker

class RoleFilter(BaseFilter):
    def __init__(self, role: Union[User.Role, list[User.Role]]) -> None:
        """
        Initialize role filter
        Args:
            role: Single role or list of roles that are allowed
        """
        self.roles = [role] if isinstance(role, User.Role) else role

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        """
        Check if user has required role
        Args:
            event: Message or CallbackQuery event
        Returns:
            bool: True if user has required role
        """
        user_id = event.from_user.id
        
        async with async_session_maker() as session:
            user = await UserDAO.find_by_telegram_id(session,user_id)
            
            if not user:
                return False
                
            return user.role in self.roles
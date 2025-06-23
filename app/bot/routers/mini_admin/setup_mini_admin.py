from aiogram import Router,F
from app.bot.routers.admin.profit_uchet_router import profic_router
from app.bot.filters.role_filter import RoleFilter
from app.db.models import User

setup_mini_admin_router = Router()

setup_mini_admin_router.message.filter(RoleFilter(User.Role.buyer.value))
setup_mini_admin_router.include_routers(
    profic_router
)
from aiogram import Router
from app.bot.filters.role_filter import RoleFilter
from app.bot.routers.foreman.object_logic.main_object_router import foreman_router
from app.bot.routers.foreman.report import report_router
from app.db.models import User

main_foreman_router = Router()
main_foreman_router.message.filter(RoleFilter(User.Role.foreman.value))
main_foreman_router.include_routers(
        foreman_router,
        report_router,
)

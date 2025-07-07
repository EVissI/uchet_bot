from aiogram import Router

from app.bot.filters.role_filter import RoleFilter
from app.db.models import User
from app.bot.routers.admin.material_reminder.setup import reminder_setup_router
from app.bot.routers.admin.profit_uchet_router import profit_router
from app.bot.routers.admin.view_material_order import material_orders_view_router
admin_buyer_setup_router = Router()

admin_buyer_setup_router.message.filter(RoleFilter([User.Role.admin.value, User.Role.buyer.value]))

admin_buyer_setup_router.include_routers(
    reminder_setup_router,
    profit_router,
    material_orders_view_router
)
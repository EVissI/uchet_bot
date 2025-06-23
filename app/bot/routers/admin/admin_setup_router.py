from aiogram import Router


from app.bot.filters.role_filter import RoleFilter
from app.db.models import User
from app.bot.routers.admin.material_reminder.setup import reminder_setup_router
from app.bot.routers.admin.notify.notify_router import admin_notify_router
from app.bot.routers.admin.tools_control.setup_tools_control import setup_tools_control_router
from app.bot.routers.admin.generate_file_id import generate_file_id_router
from app.bot.routers.admin.cheks_object import admin_reminder_object_router
from app.bot.routers.admin.finance_report import finance_report_router
from app.bot.routers.admin.profit_uchet_router import profic_router


main_admin_router = Router()
main_admin_router.message.filter(RoleFilter(User.Role.admin.value))
main_admin_router.include_routers(reminder_setup_router,
                                  admin_notify_router,
                                  setup_tools_control_router,
                                  generate_file_id_router,
                                  admin_reminder_object_router,
                                  finance_report_router,
                                  profic_router
                                  )

from aiogram import Router
from app.bot.filters.role_filter import RoleFilter
from app.bot.routers.worker.object_logic.docs_router import worker_docs_router
from app.bot.routers.worker.object_logic.checks_router import checks_router
from app.bot.routers.worker.object_logic.notify_router import notify_worker_object
from app.bot.routers.worker.object_logic.photo_from_object_router import photo_from_object_router
from app.db.models import User

main_worker_object_router = Router()
main_worker_object_router.include_routers(worker_docs_router,
                                          checks_router,
                                          notify_worker_object,
                                          photo_from_object_router)
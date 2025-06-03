from aiogram import Router
from app.bot.routers.worker.object_logic.docs_router import worker_docs_router


main__worker_object_router = Router()
main__worker_object_router.include_routers(worker_docs_router)
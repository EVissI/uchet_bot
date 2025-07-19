import asyncio
from app.bot.middlewares.logs import FSMStateLoggerMiddleware
from app.bot.routers.setup_router import main_router
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.client.default import DefaultBotProperties

from app.config import setup_logger
setup_logger("bot")

from loguru import logger
from app.db.redis import redis_client
from app.config import settings

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
admins = settings.ROOT_ADMIN_IDS
# async def set_commands():
#     commands = [
#         BotCommand(command="user_command", description="комманда юзера"),
#     ]
#     await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

#     async with async_session_maker() as session:
#         admins:list[User] = await UserDAO.find_all(session,filters=UserFilterModel(role=User.Role.admin))

#     commands.append(BotCommand(command="admin_command", description="комманда админа"))

#     # Устанавливаем команды для каждого админа отдельно
#     for admin in admins:
#         await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=admin.telegram_id))



async def start_bot():
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f"Я запущен🥳.")
        except:
            pass
    logger.info("Бот успешно запущен.")


async def stop_bot():
    await redis_client.close()
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Бот остановлен. За что?😔")
    except:
        pass
    logger.error("Бот остановлен!")


async def main():
    await redis_client.connect()
    storage = RedisStorage(
        redis_client.redis,
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

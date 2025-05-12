import asyncio
from app.bot.routers.main_router import main_router

from app.config import setup_logger
setup_logger("bot")

from loguru import logger
from app.db.models import User
from app.config import bot, admins, dp
from app.db.dao import UserDAO
from app.db.database import async_session_maker
from app.db.schemas import UserFilterModel
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_commands():
    commands = [
        BotCommand(command="user_command", description="комманда юзера"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

    async with async_session_maker() as session:
        admins:list[User] = await UserDAO.find_all(session,filters=UserFilterModel(role=User.Role.admin))

    commands.append(BotCommand(command="admin_command", description="комманда админа"))

    # Устанавливаем команды для каждого админа отдельно
    for admin in admins:
        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=admin.telegram_id))



async def start_bot():
    await set_commands()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f"Я запущен🥳.")
        except:
            pass
    logger.info("Бот успешно запущен.")


async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, "Бот остановлен. За что?😔")
    except:
        pass
    logger.error("Бот остановлен!")


async def main():
    # регистрация роутеров
    dp.include_router(main_router)

    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

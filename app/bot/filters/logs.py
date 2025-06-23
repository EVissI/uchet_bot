from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from aiogram.fsm.context import FSMContext
from loguru import logger

class FSMStateLoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state: FSMContext = data.get("state")
        user_id = None
        if hasattr(event, "from_user") and event.from_user:
            user_id = event.from_user.id
        current_state = None
        if state:
            current_state = await state.get_state()
        logger.info(
            f"[FSM] User: {user_id}, State: {current_state}, Handler: {handler.__name__}"
        )
        return await handler(event, data)
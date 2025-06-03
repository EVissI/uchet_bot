import asyncio

from typing import List
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger


class StateHistoryMixin:
    async def save_state_history(self, state: FSMContext, new_state: str) -> None:
        """Save current state to history before changing to new state"""
        data = await state.get_data()
        state_history = data.get('state_history', [])
        current = await state.get_state()
        if current:
            state_history.append(current)
        await state.update_data(state_history=state_history)
        await state.set_state(new_state)

    async def get_previous_state(self, state: FSMContext) -> str | None:
        """Get and remove last state from history"""
        data = await state.get_data()
        state_history = data.get('state_history', [])
        if state_history:
            previous_state = state_history.pop()
            await state.update_data(state_history=state_history)
            return previous_state
        return None

class DialogMessageManager:
    async def save_message(self, state: FSMContext, message_id: int) -> None:
        """Save message ID to state"""
        data = await state.get_data()
        message_ids = data.get('dialog_messages', [])
        message_ids.append(message_id)
        await state.update_data(dialog_messages=message_ids)


    async def delete_message(self, bot: Bot, chat_id: int, message_id: int) -> bool:
        """Delete single message with error handling"""
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            return True
        except Exception as e:
            return False

    async def clear_messages(self, state: FSMContext, chat_id: int, bot: Bot) -> None:
        """Delete all saved messages concurrently"""
        data = await state.get_data()
        message_ids = data.get('dialog_messages', [])
        
        if message_ids:
            delete_tasks = [
                self.delete_message(bot, chat_id, msg_id) 
                for msg_id in message_ids
            ]
            
            results = await asyncio.gather(*delete_tasks, return_exceptions=True)
            
            successful = sum(1 for r in results if r is True)
            failed = len(message_ids) - successful
            if failed > 0:
                logger.warning(f"Failed to delete {failed} out of {len(message_ids)} messages")
            
        await state.update_data(dialog_messages=[])
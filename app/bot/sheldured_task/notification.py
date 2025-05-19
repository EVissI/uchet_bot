from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger


from app.config import bot
from app.db.database import async_session_maker
from app.db.models import WorkerNotification, ForemanNotification, User
from app.db.dao import UserDAO,ForemanNotificationDAO,WorkerNotificationDAO
from app.db.schemas import UserFilterModel,NotificationFilter

async def send_worker_notifications():
    """Send notifications to workers"""
    async with async_session_maker() as session:
        notifications: WorkerNotification = await WorkerNotificationDAO.find_one_or_none(session,filters=NotificationFilter())
        
        workers = await UserDAO.find_all(
            session, 
            UserFilterModel(role=User.Role.worker, can_use_bot=True)
        )
        
        for worker in workers:
            try:
                await bot.send_message(
                    chat_id=worker.telegram_id,
                    text=notifications.message,
                )
            except Exception as e:
                logger.error(f"Error sending notification to worker {worker.telegram_id}: {e}")
                continue

async def send_foreman_notifications():
    """Send notifications to foremen"""
    async with async_session_maker() as session:
        notifications: ForemanNotification = await ForemanNotificationDAO.find_one_or_none(session,filters=NotificationFilter())

        
        foremen = await UserDAO.find_all(
            session, 
            UserFilterModel(role=User.Role.foreman, can_use_bot=True)
        )
        
        for foreman in foremen:
            try:
                await bot.send_message(
                    chat_id=foreman.telegram_id,
                    text=notifications.message,
                )
            except Exception as e:
                logger.error(f"Error sending notification to foreman {foreman.telegram_id}: {e}")
                continue

async def setup_notification_tasks(scheduler: AsyncIOScheduler):
    """Setup notification tasks"""
    async with async_session_maker as session:
        notifications_worker: WorkerNotification = await WorkerNotificationDAO.find_one_or_none(
            session,
            filters=NotificationFilter()
        )
        notifications_foreman: ForemanNotification = await ForemanNotificationDAO.find_one_or_none(
            session,
            filters=NotificationFilter()
        )

        if notifications_worker:
            # First worker notification
            scheduler.add_job(
                send_worker_notifications,
                trigger=CronTrigger(
                    hour=notifications_worker.first_notification_time.hour,
                    minute=notifications_worker.first_notification_time.minute
                ),
                id='worker_notifications_first',
                replace_existing=True
            )

            # Second worker notification
            scheduler.add_job(
                send_worker_notifications,
                trigger=CronTrigger(
                    hour=notifications_worker.second_notification_time.hour,
                    minute=notifications_worker.second_notification_time.minute
                ),
                id='worker_notifications_second',
                replace_existing=True
            )

        if notifications_foreman:
            # First foreman notification
            scheduler.add_job(
                send_foreman_notifications,
                trigger=CronTrigger(
                    hour=notifications_foreman.first_notification_time.hour,
                    minute=notifications_foreman.first_notification_time.minute
                ),
                id='foreman_notifications_first',
                replace_existing=True
            )

            # Second foreman notification
            scheduler.add_job(
                send_foreman_notifications,
                trigger=CronTrigger(
                    hour=notifications_foreman.second_notification_time.hour,
                    minute=notifications_foreman.second_notification_time.minute
                ),
                id='foreman_notifications_second',
                replace_existing=True
            )
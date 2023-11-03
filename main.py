import asyncio
import logging
import aioschedule

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from aiogram import Dispatcher

from settings.config import Configuration
from database.db import DatabaseManager
from handlers import (start_handler, 
                    profile_handler,
                    admin_handler, 
                    slot_game_handler,
                    currency_handler, 
                    other_handlers)

async def start():
    """
    Configure logging, create a bot instance, initialize a dispatcher,
    include the router, start polling, and close the bot session.
    """

    # Initialize a bot
    conf = Configuration()
    bot = conf.bot
    db = DatabaseManager()
    
    # Configure logging
    logging.basicConfig(
        level=1,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('logging.log', encoding='utf-8'),
            logging.StreamHandler()
            ]
    )

    # Initialize a dispatcher
    dp = Dispatcher()
    
    # Initialize the database
    dp.startup.register(db.db_start)

    # Initialize a scheduler
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(db.give_daily_bonus, 'cron', hour=00, minute=1, start_date = datetime.now())
    scheduler.start()

    # Include the router
    dp.include_routers(
                start_handler.router,
                admin_handler.router,
                profile_handler.router,
                slot_game_handler.router,
                currency_handler.router,
                other_handlers.router)

    try:
        # Start polling
        logging.info('Bot started')
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Close the bot session
        await bot.session.close()
        
if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info('Bot stopped\n\n')
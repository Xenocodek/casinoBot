import asyncio
import logging

from aiogram import Dispatcher

from settings.config import Configuration
from database import requests as db
from handlers import cmd_handlers, other_handlers

async def start():
    """
    Configure logging, create a bot instance, initialize a dispatcher,
    include the router, start polling, and close the bot session.
    """

    # Initialize a bot
    conf = Configuration()
    bot = conf.bot
    
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

    # Include the router
    dp.include_routers(
                cmd_handlers.router,
                other_handlers.router)

    await db.db_start()

    try:
        # Start polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        # Close the bot session
        await bot.session.close()
        
if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info('Bot stopped\n')
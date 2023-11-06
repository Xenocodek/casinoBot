import os

from aiogram import Bot

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    """Bot configuration."""

    token: str = os.getenv("API_TOKEN")


@dataclass
class DatabaseConfig:
    """Database Config."""

    host: str = os.getenv("MYSQLHOST")
    port = int(os.getenv("MYSQLPORT", 22085))
    user: str = os.getenv("MYSQLUSER")
    password: str = os.getenv("MYSQLPASSWORD")
    database: str = os.getenv("MYSQL_DATABASE")


@dataclass
class Configuration:
    """All in one configuration's class."""

    botconfig = BotConfig()

    bot = Bot(token=botconfig.token, parse_mode='HTML')


@dataclass
class ExchangeManager:
    """Exchange manager."""

    token: str = os.getenv("EXCHANGE_TOKEN")


@dataclass
class WeatherManager:
    """Exchange manager."""

    token: str = os.getenv("WEATHER_TOKEN")
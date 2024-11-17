import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message
import requests

# Токен Telegram-бота
TELEGRAM_TOKEN = "7354571535:AAGesDE_dHUd90nsixHF2FiIQCqGol9oe5k"

# API-ключ OpenWeather
OPENWEATHER_API_KEY = "74badfd98e93ccbefa3b88eb58dc9abf"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Функция для получения погоды
def get_weather(city="Иркутск"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPENWEATHER_API_KEY}&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в {city}:\nТемпература: {temp}°C\nОписание: {description.capitalize()}"
    else:
        return "Не удалось получить прогноз погоды. Проверьте правильность названия города."

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я погодный бот.\n"
        "Напиши /weather, чтобы узнать погоду в Иркутске.\n"
        "Или отправь /weather <название_города>, чтобы узнать погоду в другом месте."
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: Message):
    await message.answer(
        "Я могу показывать погоду. Вот что я умею:\n"
        "/start - Запуск бота\n"
        "/help - Справка\n"
        "/weather - Погода в Иркутске\n"
        "/weather <город> - Погода в указанном городе"
    )

# Обработчик команды /weather
@dp.message(Command("weather"))
async def send_weather(message: Message, command: CommandObject):
    city = command.args if command.args else "irkutsk"  # Если аргумент отсутствует, используем "Иркутск"
    weather_info = get_weather(city)
    await message.answer(weather_info)

# Основная функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
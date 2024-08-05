import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers.handlers import register_handlers

logging.basicConfig(level=logging.INFO)


async def handle_root(request):
    return web.Response(text="Bot is running")


async def handle_webhook_get(request):
    return web.Response(text="Webhook is set up and working.")


async def on_startup(app):
    bot = app['bot']
    webhook_url = WEBHOOK_URL + WEBHOOK_PATH
    await bot.set_webhook(webhook_url)
    logging.info(f"Bot started and webhook set to {webhook_url}")


async def on_shutdown(app):
    bot = app['bot']
    await bot.session.close()
    logging.info("Bot stopped")


async def handle_message(message: types.Message):
    try:
        await message.answer("Received your message")
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    register_handlers(dp)

    app = web.Application()
    app['bot'] = bot

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Добавляем корневой роутер
    app.router.add_route('*', '/', handle_root)

    # Добавляем GET-обработчик для /webhook
    app.router.add_get(WEBHOOK_PATH, handle_webhook_get)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

if __name__ == '__main__':
    app = asyncio.run(main())
    web.run_app(app, host='0.0.0.0', port=8000)

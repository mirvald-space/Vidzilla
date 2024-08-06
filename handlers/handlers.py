import re

from aiogram import Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from handlers.facebook import process_facebook
from handlers.instagram import process_instagram
from handlers.tiktok import process_tiktok
from handlers.youtube import process_youtube


class DownloadVideo(StatesGroup):
    waiting_for_link = State()


async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("👋 Hi! I can download videos from Instagram Reels and TikTok. "
                         "Available commands:\n\n"
                         "/start - start working with the bot\n"
                         "/help - get help\n\n"
                         "Just send me a video link, and I'll return it as a video message and a file.")
    await state.set_state(DownloadVideo.waiting_for_link)


async def send_help(message: types.Message):
    await message.answer("This bot helps download videos from Instagram Reels and TikTok.\n\n"
                         "How to use:\n"
                         "1. Send the bot a link to a video from Instagram Reels or TikTok.\n"
                         "2. The bot will process the link and return the video in two formats:\n"
                         "   - As a video message\n"
                         "   - As a document file\n\n"
                         "Supported services:\n"
                         "- Instagram Reels\n"
                         "- TikTok\n\n"
                         "Commands:\n"
                         "/start - start working with the bot\n"
                         "/help - show this help message")


async def process_link(message: Message, state: FSMContext, bot: Bot):
    url = message.text
    await message.answer("Processing your link...")
    try:
        if 'instagram.com' in url:
            await process_instagram(message, bot, url)
        elif 'tiktok.com' in url:
            await process_tiktok(message, bot, url)
        elif 'youtube.com' in url or 'youtu.be' in url:
            await process_youtube(message, bot, url)
        elif 'facebook.com' in url:
            await process_facebook(message, bot, url)
        else:
            await message.answer("Unsupported platform. Please provide a link from Instagram, TikTok, or YouTube.")
    except Exception as e:
        await message.answer(f"Error processing video: {str(e)}")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(send_help, Command(commands=['help']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)

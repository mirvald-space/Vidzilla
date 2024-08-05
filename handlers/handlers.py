import re

from aiogram import Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import RAPIDAPI_HOST, RAPIDAPI_KEY
from handlers.instagram import process_instagram
from handlers.tiktok import process_tiktok
from utils import get_video_url


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


async def process_link(message: types.Message, state: FSMContext, bot: Bot):
    url = message.text
    await message.answer("Processing your link...")

    if 'instagram.com' in url:
        url = re.sub(r'\?.*$', '', url)

    api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"
    querystring = {"url": url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        video_url = await get_video_url(api_url, headers, querystring)
    except Exception as e:
        await message.answer(f"Error getting video URL: {str(e)}")
        await state.clear()
        await state.set_state(DownloadVideo.waiting_for_link)
        return

    if video_url:
        if 'instagram.com' in url:
            await process_instagram(message, bot, url)
        elif 'tiktok.com' in url:
            await process_tiktok(message, bot, video_url)
        else:
            await message.answer("Unsupported platform.")
    else:
        await message.answer("Couldn't find a link to the video.")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(send_help, Command(commands=['help']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)

import aiohttp
from aiogram import Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import SendDocument
from aiogram.types import BufferedInputFile, FSInputFile, URLInputFile

from config import RAPIDAPI_HOST, RAPIDAPI_KEY
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

    api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"
    querystring = {"url": url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    video_url = await get_video_url(api_url, headers, querystring)

    if video_url:
        try:
            # Создаем URLInputFile для видео
            video_file = URLInputFile(video_url)

            # Отправляем как видео
            await message.answer_video(
                video_file,
                width=720,
                height=1280,
                duration=60,  # Предполагаемая продолжительность, замените на реальную если возможно
                supports_streaming=True
            )

            # Отправляем как обычный файл
            file_name = f"video_{message.from_user.id}.mp4"
            doc_file = URLInputFile(video_url, filename=file_name)

            await bot.send_document(
                chat_id=message.chat.id,
                document=doc_file,
                disable_content_type_detection=True
            )

        except Exception as e:
            await message.answer(f"Failed to send the video: {str(e)}")
    else:
        await message.answer("Couldn't find a link to the video.")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(send_help, Command(commands=['help']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)

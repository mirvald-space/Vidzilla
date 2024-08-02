from aiogram.types import URLInputFile
from aiogram import Bot
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
    await message.answer("Привет. Отправь мне ссылку на видео из Instagram Reels или TikTok, и я верну тебе это видео в виде видеосообщения и файла-документа.")
    await state.set_state(DownloadVideo.waiting_for_link)


async def process_link(message: types.Message, state: FSMContext, bot: Bot):
    url = message.text
    await message.answer("Обрабатываю вашу ссылку...")

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
                caption="Your video file",
                disable_content_type_detection=True
            )

        except Exception as e:
            await message.answer(f"Не удалось отправить видео: {str(e)}")
    else:
        await message.answer("Не удалось найти ссылку на видео.")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start', 'help']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)

from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile

from config import RAPIDAPI_HOST, RAPIDAPI_KEY
from utils import download_video, get_video_url


class DownloadVideo(StatesGroup):
    waiting_for_link = State()


async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Hi. Send me a link to an Instagram Reel or TikTok video and I'll get the video back to you.")
    await state.set_state(DownloadVideo.waiting_for_link)


async def process_link(message: types.Message, state: FSMContext):
    url = message.text
    await message.reply("Processing your link...")

    api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"
    querystring = {"url": url}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    video_url = await get_video_url(api_url, headers, querystring)

    if video_url:
        video_content = await download_video(video_url)
        if video_content:
            video_file = BufferedInputFile(video_content, filename="video.mp4")
            await message.reply_video(video_file)
        else:
            await message.reply("Failed to download the video.")
    else:
        await message.reply("Couldn't find a link to the video.")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start', 'help']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)

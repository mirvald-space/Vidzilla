import asyncio
import os

import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hi. Send me a link to a TikTok or Instagram video and I'll download it in the best quality available and send it as a file.")


@dp.message()
async def handle_video_link(message: types.Message):
    if "tiktok.com" in message.text or "instagram.com" in message.text:
        await message.answer("Processing your link...")

        try:
            ydl_opts = {
                'outtmpl': f'video_{message.from_user.id}.%(ext)s',
                'format': 'bestvideo+bestaudio/best',  # Выбор наилучшего качества
                'merge_output_format': 'mp4',  # Объединение аудио и видео в mp4
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                file_name = ydl.prepare_filename(info)

            if os.path.exists(file_name):
                file_size = os.path.getsize(
                    file_name) / (1024 * 1024)  # Размер в МБ

                # Отправляем сообщение отдельно
                await message.answer(f"Here is your video in the best quality available. File size: {file_size:.2f} MB")

                # Отправляем видео пользователю как документ без подписи
                document = FSInputFile(file_name)
                await message.answer_document(document, disable_content_type_detection=True)

                # Удаляем временный файл
                os.remove(file_name)
            else:
                await message.answer("Sorry, failed to download the video. Please try another link.")
        except Exception as e:
            await message.answer(f"An error occurred while processing the request: {str(e)}")
    else:
        await message.answer("Please send the correct link to the TikTok or Instagram video.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

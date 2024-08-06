import asyncio
import logging
import os

import yt_dlp
from aiogram import Bot
from aiogram.types import FSInputFile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Путь к папке, где будут временно храниться загруженные файлы
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "temp_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def download_instagram_content(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': {
            'default': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        },
        'ignore_no_formats': True,
        'verbose': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            if info is None:
                logger.warning("No information extracted from the URL")
                return None

            filename = ydl.prepare_filename(info)

            if os.path.exists(filename):
                logger.info(f"Video downloaded successfully: {filename}")
                return filename
            else:
                logger.warning(
                    f"Video file not found after download: {filename}")
                return None

    except Exception as e:
        logger.exception(f"Error downloading Instagram content: {str(e)}")
        return None


async def process_instagram(message, bot: Bot, instagram_url: str):
    try:
        logger.info(f"Processing Instagram URL: {instagram_url}")

        # Загружаем контент
        video_path = await download_instagram_content(instagram_url)

        if video_path and os.path.exists(video_path):
            logger.info(f"Video available at: {video_path}")

            file_size = os.path.getsize(video_path)
            logger.info(f"File size: {file_size} bytes")

            try:
                # Отправляем видео
                video_file = FSInputFile(video_path)
                sent_video = await bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    # caption="Here's your Instagram video!"
                )
                logger.info(f"Video sent successfully. Message ID: {
                            sent_video.message_id}")

                # Отправляем видео как документ
                doc_filename = f"instagram_video_{message.from_user.id}.mp4"
                doc_file = FSInputFile(video_path, filename=doc_filename)
                sent_document = await bot.send_document(
                    chat_id=message.chat.id,
                    document=doc_file,
                    # caption="Here's your Instagram video as a file!",
                    disable_content_type_detection=True
                )
                logger.info(f"Video document sent successfully. Message ID: {
                            sent_document.message_id}")

            except Exception as send_error:
                logger.exception(f"Error sending content: {str(send_error)}")
                await message.reply(f"Error sending content: {str(send_error)}")
            finally:
                # Удаляем временный файл
                try:
                    os.remove(video_path)
                    logger.info(f"Temporary file deleted: {video_path}")
                except Exception as delete_error:
                    logger.exception(f"Error deleting temporary file: {
                                     str(delete_error)}")
        else:
            logger.warning("No video content available.")
            await message.reply("This Instagram post is not a video or the video couldn't be downloaded.")

    except Exception as e:
        logger.exception(f"Error processing Instagram content: {str(e)}")
        await message.reply(f"Error processing Instagram content: {str(e)}")

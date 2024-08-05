import asyncio
import os

import yt_dlp
from aiogram.types import FSInputFile


async def download_instagram_video(url, output_path):
    loop = asyncio.get_event_loop()
    try:
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best',
        }
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        return True
    except Exception as e:
        print(f"Error downloading Instagram video: {str(e)}")
        return False


async def process_instagram(message, bot, url):
    file_name = f"instagram_video_{message.from_user.id}.mp4"
    download_success = await download_instagram_video(url, file_name)

    if download_success:
        try:
            # Отправляем видео
            await message.answer_video(
                FSInputFile(file_name),
                caption="Here's your Instagram video!"
            )

            # Отправляем как документ
            await bot.send_document(
                chat_id=message.chat.id,
                document=FSInputFile(file_name),
                caption="Here's your Instagram video as a file!",
                disable_content_type_detection=True
            )
        except Exception as e:
            await message.answer(f"Error sending Instagram video: {str(e)}")
        finally:
            # Удаляем временный файл
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"Error removing temporary file: {str(e)}")
    else:
        await message.answer("Failed to download Instagram video.")

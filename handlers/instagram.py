import os
import time

import ddinsta
from aiogram.types import FSInputFile

from config import TEMP_DIRECTORY

# Убедимся, что временная директория существует
os.makedirs(TEMP_DIRECTORY, exist_ok=True)


async def process_instagram(message, bot, instagram_url):
    try:
        # Генерируем уникальное имя файла
        temp_file_name = f"temp_video_{
            message.from_user.id}_{int(time.time())}.mp4"
        temp_file_path = os.path.join(TEMP_DIRECTORY, temp_file_name)

        # Download video using ddinsta
        result = ddinsta.save_video(instagram_url)

        if result == '[!] Success':
            # Ищем последний созданный файл в текущей директории
            files = [f for f in os.listdir('.') if f.endswith('.mp4')]
            if files:
                latest_file = max(files, key=os.path.getctime)
                # Перемещаем файл в нашу временную директорию
                os.rename(latest_file, temp_file_path)

                # Send video
                video_file = FSInputFile(temp_file_path)
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file
                )

                # Send as document
                file_name = f"instagram_video_{message.from_user.id}.mp4"
                doc_file = FSInputFile(temp_file_path, filename=file_name)
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=doc_file,
                    disable_content_type_detection=True
                )

                # Clean up the temporary file
                os.remove(temp_file_path)
            else:
                await bot.send_message(message.chat.id, "Error: Video file not found after download")
        else:
            await bot.send_message(message.chat.id, f"Error: Failed to retrieve the video from Instagram. {result}")
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error processing Instagram video: {str(e)}")

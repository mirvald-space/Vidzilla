from aiogram.types import URLInputFile


async def process_tiktok(message, bot, video_url):
    try:
        # Отправляем видео
        video_file = URLInputFile(video_url)
        await message.answer_video(
            video_file,
            caption="Here's your TikTok video!"
        )

        # Отправляем как документ
        file_name = f"tiktok_video_{message.from_user.id}.mp4"
        doc_file = URLInputFile(video_url, filename=file_name)
        await bot.send_document(
            chat_id=message.chat.id,
            document=doc_file,
            caption="Here's your TikTok video as a file!",
            disable_content_type_detection=True
        )
    except Exception as e:
        await message.answer(f"Error processing TikTok video: {str(e)}")

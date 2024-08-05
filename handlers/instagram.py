from aiogram.types import URLInputFile
from aiohttp import ClientSession

from config import RAPIDAPI_HOST, RAPIDAPI_KEY


async def process_instagram(message, bot, instagram_url):
    try:
        api_url = "https://social-media-video-downloader.p.rapidapi.com/smvd/get/all"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        querystring = {"url": instagram_url}

        async with ClientSession() as session:
            async with session.get(api_url, headers=headers, params=querystring) as response:
                if response.status == 200:
                    data = await response.json()
                    video_url = await get_video_url(data)
                else:
                    await message.answer(f"Ошибка API: HTTP {response.status}")
                    return

        if video_url:
            # Отправляем видео
            video_file = URLInputFile(video_url)
            await message.answer_video(
                video_file,
                caption="Here's your Instagram video!"
            )

            # Отправляем как документ
            file_name = f"instagram_video_{message.from_user.id}.mp4"
            doc_file = URLInputFile(video_url, filename=file_name)
            await bot.send_document(
                chat_id=message.chat.id,
                document=doc_file,
                caption="Here's your Instagram video as a file!",
                disable_content_type_detection=True
            )
        else:
            await message.answer("Не удалось получить URL видео.")
    except Exception as e:
        await message.answer(f"Ошибка при обработке видео из Instagram: {str(e)}")


async def get_video_url(data):
    if data['success']:
        if 'links' in data:
            if isinstance(data['links'], list):
                video_url = next((link['link'] for link in data['links'] if link['quality']
                                 == 'video_hd_original' or link['quality'] == 'video_hd_original_0'), None)
                if not video_url:
                    video_url = next(
                        (link['link'] for link in data['links'] if 'video' in link['quality'].lower()), None)
                return video_url
    return None

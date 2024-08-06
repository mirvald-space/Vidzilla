import json

import aiohttp
from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY


async def process_instagram(message, bot, instagram_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://instagram-media-downloader.p.rapidapi.com/rapid/post_v2.php",
                                   params={"url": instagram_url},
                                   headers={
                                       "X-RapidAPI-Key": RAPIDAPI_KEY,
                                       "X-RapidAPI-Host": "instagram-media-downloader.p.rapidapi.com"
                                   }) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Full API response: {json.dumps(data, indent=2)}")

                    if 'items' in data and len(data['items']) > 0:
                        item = data['items'][0]
                        if 'video_versions' in item and len(item['video_versions']) > 0:
                            video_url = item['video_versions'][0]['url']
                            caption = item['caption']['text'] if 'caption' in item and item['caption'] else ""

                            # Отправка видео
                            video_file = URLInputFile(video_url)
                            await bot.send_video(
                                chat_id=message.chat.id,
                                video=video_file,
                                caption=caption
                            )

                            # Отправка видео как документа
                            file_name = f"instagram_video_{
                                message.from_user.id}.mp4"
                            doc_file = URLInputFile(
                                video_url, filename=file_name)
                            await bot.send_document(
                                chat_id=message.chat.id,
                                document=doc_file,
                                caption="Вот ваше Instagram видео в виде файла",
                                disable_content_type_detection=True
                            )
                        else:
                            await bot.send_message(message.chat.id, "Это публикация не содержит видео.")
                    else:
                        await bot.send_message(message.chat.id, "Не удалось найти медиа в ответе API.")
                else:
                    error_message = await response.text()
                    await bot.send_message(message.chat.id, f"API Error: HTTP {response.status}\nDetails: {error_message}")
    except Exception as e:
        await bot.send_message(message.chat.id, f"Ошибка при обработке Instagram видео: {str(e)}")

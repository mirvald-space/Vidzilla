import json

import aiohttp
from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY


async def process_facebook(message, bot, youtube_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://social-media-video-downloader.p.rapidapi.com/smvd/get/all",
                                   params={"url": youtube_url},
                                   headers={
                                       "X-RapidAPI-Key": RAPIDAPI_KEY,
                                       "X-RapidAPI-Host": "social-media-video-downloader.p.rapidapi.com"
                                   }) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Full API response: {json.dumps(data, indent=2)}")

                    if data.get('success') and data.get('links'):
                        video_url = next(
                            (link['link'] for link in data['links']
                             if 'video' in link['quality'] and 'only_video' not in link['quality']),
                            None
                        )
                        if not video_url:
                            video_url = data['links'][0]['link']
                    else:
                        await bot.send_message(message.chat.id, f"Failed to retrieve the URL of the video. API response: {json.dumps(data, indent=2)}")
                        return
                else:
                    error_message = await response.text()
                    await bot.send_message(message.chat.id, f"API Error: HTTP {response.status}\nDetails: {error_message}")
                    return

        if video_url:
            video_file = URLInputFile(video_url)
            await bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
                # caption=f"Here's your Facebook video: {data['title']}"
            )
            file_name = f"facebook_video_{message.from_user.id}.mp4"
            doc_file = URLInputFile(video_url, filename=file_name)
            await bot.send_document(
                chat_id=message.chat.id,
                document=doc_file,
                # caption=f"Here's your Facebook video as a file: {
                #     data['title']}",
                disable_content_type_detection=True
            )
        else:
            await bot.send_message(message.chat.id, "Failed to retrieve the URL of the video.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error processing Facebook video: {str(e)}")

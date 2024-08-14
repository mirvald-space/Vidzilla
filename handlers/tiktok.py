import json

import requests
from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY


async def process_tiktok(message, bot, tiktok_url):
    try:
        url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
        payload = {"url": tiktok_url}
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        if response.status_code == 200 and 'medias' in data and len(data['medias']) > 0:
            video_url = data['medias'][0]['url']

            video_file = URLInputFile(video_url)
            await bot.send_video(
                chat_id=message.chat.id,
                video=video_file
            )

            file_name = f"tiktok_video{message.from_user.id}.mp4"
            doc_file = URLInputFile(video_url, filename=file_name)
            await bot.send_document(
                chat_id=message.chat.id,
                document=doc_file,
                disable_content_type_detection=True
            )
        else:
            error_message = data.get(
                'message', 'Failed to retrieve the video from TikTok')
            await bot.send_message(message.chat.id, f"Error: {error_message}")

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error processing Tiktok video: {str(e)}")

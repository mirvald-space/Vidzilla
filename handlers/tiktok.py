import http.client
import json
from urllib.parse import urlencode

from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY


async def process_tiktok(message, bot, tiktok_url):
    try:
        conn = http.client.HTTPSConnection(
            "social-media-video-downloader.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': "social-media-video-downloader.p.rapidapi.com"
        }

        querystring = urlencode({"url": tiktok_url})

        conn.request("GET", f"/smvd/get/all?{querystring}", headers=headers)

        response = conn.getresponse()

        if response.status == 200:
            data = json.loads(response.read().decode())

            print(f"Full API response: {json.dumps(data, indent=2)}")

            if 'links' in data and len(data['links']) > 0:
                video_url = data['links'][0]['link']
            else:
                await bot.send_message(message.chat.id, f"Failed to retrieve the URL of the video. API response: {json.dumps(data, indent=2)}")
                return
        else:
            error_message = response.read().decode()
            await bot.send_message(message.chat.id, f"API Error: HTTP {response.status}\nDetails: {error_message}")
            return

        if video_url:
            video_file = URLInputFile(video_url)
            await bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
                # caption="Here's your TikTok video!"
            )

            file_name = f"tiktok_video_{message.from_user.id}.mp4"
            doc_file = URLInputFile(video_url, filename=file_name)
            await bot.send_document(
                chat_id=message.chat.id,
                document=doc_file,
                # caption="Here's your TikTok video as a file!",
                disable_content_type_detection=True
            )
        else:
            await bot.send_message(message.chat.id, "Failed to retrieve the URL of the video.")

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error processing TikTok video: {str(e)}")
    finally:
        conn.close()

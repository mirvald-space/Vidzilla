import logging
import os

import aiohttp
from aiogram import Bot
from aiogram.types import URLInputFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAPIDAPI_KEY = os.getenv(
    'RAPIDAPI_KEY', 'a267530cf0msheda24d8f8243cbbp177eabjsnaeb3c18b82da')
RAPIDAPI_HOST = "all-media-downloader.p.rapidapi.com"
API_URL = "https://all-media-downloader.p.rapidapi.com/rapid_download/download"


async def process_instagram(message, bot: Bot, instagram_url: str):
    try:
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n{
            instagram_url}\r\n-----011000010111000001101001--\r\n\r\n"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST,
            "Content-Type": "multipart/form-data; boundary=---011000010111000001101001"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, data=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"API response: {data}")

                    if 'result' in data and data['result']:
                        video_url = data['result']['downloadUrl']
                        caption = data['result'].get(
                            'caption', 'Instagram video')

                        # Send as video
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=video_url,
                            # Limit caption to 1024 characters
                            caption=caption[:1024]
                        )
                        logger.info(
                            f"Video sent successfully as video message")

                        # Send as document
                        await bot.send_document(
                            chat_id=message.chat.id,
                            document=URLInputFile(
                                video_url, filename="instagram_video.mp4"),
                            caption=f"{caption[:1024]} (as document)",
                            disable_content_type_detection=True
                        )
                        logger.info(f"Video sent successfully as document")
                    else:
                        await bot.send_message(chat_id=message.chat.id, text="No video found in the Instagram post. This might be an image post or the API couldn't process it.")
                else:
                    error_message = await response.text()
                    logger.error(f"API Error: HTTP {
                                 response.status}\nDetails: {error_message}")
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"There was an error processing your Instagram link. Please try again later."
                    )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="An unexpected error occurred while processing your request. "
                 "Please try again later or contact support if the issue persists."
        )

# Optionally, you can add a function to handle Instagram stories if needed
# async def process_instagram_story(message, bot: Bot, username: str):
#     # Implementation for downloading and sending Instagram stories
#     pass

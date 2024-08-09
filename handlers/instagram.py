import json
import logging

import requests
from aiogram import Bot
from aiogram.types import FSInputFile

from config import RAPIDAPI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instagram(message, bot: Bot, instagram_url: str):
    try:
        url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

        querystring = {"url": instagram_url}

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            logger.info(f"API response: {json.dumps(data, indent=2)}")

            if 'media' in data:
                video_url = data['media']
                caption = data.get('title', 'Instagram video')

                try:
                    await bot.send_video(
                        chat_id=message.chat.id,
                        video=video_url,
                        caption=caption
                    )
                    logger.info(
                        f"Video sent successfully as video message: {video_url}")

                    video_response = requests.get(video_url)
                    if video_response.status_code == 200:
                        with open('temp_video.mp4', 'wb') as file:
                            file.write(video_response.content)

                        video_file = FSInputFile('temp_video.mp4')
                        await bot.send_document(
                            chat_id=message.chat.id,
                            document=video_file,
                            caption=f"{caption} (as document)",
                            disable_content_type_detection=True
                        )
                        logger.info(
                            f"Video sent successfully as document: {video_url}")
                    else:
                        logger.error(f"Failed to download video: HTTP {
                                     video_response.status_code}")
                        await bot.send_message(chat_id=message.chat.id, text="Failed to download video for document sending.")

                except Exception as send_error:
                    logger.error(f"Error sending video: {str(send_error)}")
                    await bot.send_message(chat_id=message.chat.id, text=f"Error sending video: {str(send_error)}")
            else:
                await bot.send_message(chat_id=message.chat.id, text="No video found in the Instagram post.")
        else:
            error_message = response.text
            logger.error(f"API Error: HTTP {
                         response.status_code}\nDetails: {error_message}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"There was an error processing your request (HTTP {
                    response.status_code}). "
                "Please try again later or contact support if the issue persists."
            )
    except requests.RequestException as request_error:
        logger.error(f"Network error: {str(request_error)}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="There was a network error while trying to process your request. "
            "Please check your internet connection and try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="An unexpected error occurred while processing your request. "
            "Please try again later or contact support if the issue persists."
        )

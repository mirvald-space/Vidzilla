import json
import logging

import aiohttp
from aiogram import Bot

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

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                if response.status == 200:
                    data = await response.json()
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
                                f"Video sent successfully: {video_url}")
                        except Exception as send_error:
                            logger.error(f"Error sending video: {
                                         str(send_error)}")
                            await bot.send_message(chat_id=message.chat.id, text=f"Error sending video: {str(send_error)}")
                    else:
                        await bot.send_message(chat_id=message.chat.id, text="No video found in the Instagram post.")
                else:
                    error_message = await response.text()
                    logger.error(f"API Error: HTTP {
                                 response.status}\nDetails: {error_message}")
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"There was an error processing your request (HTTP {
                            response.status}). "
                        "Please try again later or contact support if the issue persists."
                    )
    except aiohttp.ClientError as client_error:
        logger.error(f"Network error: {str(client_error)}")
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

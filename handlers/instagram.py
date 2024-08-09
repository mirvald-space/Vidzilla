import json
import logging
from typing import List

import aiohttp
from aiogram import Bot
from aiogram.types import InputMediaVideo

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

                    videos = []
                    if data.get('Type') == 'Carousel':
                        for item in data.get('media_with_thumb', []):
                            if item['Type'] == 'Video':
                                videos.append(item['media'])
                    elif 'media' in data and isinstance(data['media'], list):
                        videos = [url for url in data['media']
                                  if 'video' in url.lower()]
                    elif 'video' in data:
                        videos = [data['video']]

                    if videos:
                        caption = data.get('title', 'Instagram video')
                        for video_url in videos:
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
                        await bot.send_message(chat_id=message.chat.id, text="No videos found in the Instagram post.")
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

import json
import logging

import aiohttp
from aiogram.types import MediaGroup, URLInputFile

from config import RAPIDAPI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instagram(message, bot, instagram_url):
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

                    if data.get('Type') == 'Carousel':
                        media_group = MediaGroup()
                        # Telegram allows max 10 items in a group
                        for item in data.get('media_with_thumb', [])[:10]:
                            if item['Type'] == 'Image':
                                media_group.attach_photo(item['media'], caption=data['title'] if len(
                                    media_group.media) == 0 else '')
                            elif item['Type'] == 'Video':
                                media_group.attach_video(item['media'], caption=data['title'] if len(
                                    media_group.media) == 0 else '')

                        if media_group.media:
                            await bot.send_media_group(message.chat.id, media=media_group)
                            logger.info("Carousel media sent successfully")
                        else:
                            await bot.send_message(message.chat.id, "No media found in the carousel.")
                    elif 'media' in data:
                        media_url = data['media'][0] if isinstance(
                            data['media'], list) else data['media']
                        caption = data.get('title', 'Instagram media')

                        try:
                            media_file = URLInputFile(media_url)
                            if 'video' in data:
                                await bot.send_video(
                                    chat_id=message.chat.id,
                                    video=media_file,
                                    caption=caption
                                )
                            else:
                                await bot.send_photo(
                                    chat_id=message.chat.id,
                                    photo=media_file,
                                    caption=caption
                                )
                            logger.info("Media sent successfully")
                        except Exception as send_error:
                            logger.error(f"Error sending media: {
                                         str(send_error)}")
                            await bot.send_message(message.chat.id, f"Error sending media: {str(send_error)}")
                    else:
                        await bot.send_message(message.chat.id, "No media found in the response.")
                else:
                    error_message = await response.text()
                    logger.error(f"API Error: HTTP {
                                 response.status}\nDetails: {error_message}")
                    await bot.send_message(
                        message.chat.id,
                        f"There was an error processing your request (HTTP {
                            response.status}). "
                        "Please try again later or contact support if the issue persists."
                    )
    except aiohttp.ClientError as client_error:
        logger.error(f"Network error: {str(client_error)}")
        await bot.send_message(
            message.chat.id,
            "There was a network error while trying to process your request. "
            "Please check your internet connection and try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await bot.send_message(
            message.chat.id,
            "An unexpected error occurred while processing your request. "
            "Please try again later or contact support if the issue persists."
        )

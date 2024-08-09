import json
import logging

import aiohttp
from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instagram(message, bot, instagram_url):
    try:
        url = "https://instagram-video-or-images-downloader.p.rapidapi.com/"

        payload = {"url": instagram_url}

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-video-or-images-downloader.p.rapidapi.com",
            "content-type": "application/x-www-form-urlencoded"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"API response: {json.dumps(data, indent=2)}")

                    if data['status'] and data['code'] == 200:
                        response_data = data['response']
                        if 'links' in response_data and len(response_data['links']) > 0:
                            video_url = response_data['links'][0]['url']
                            video_title = response_data['title']
                            logger.info(
                                f"Attempting to access video URL: {video_url}")

                            try:
                                video_file = URLInputFile(video_url)
                                await bot.send_video(
                                    chat_id=message.chat.id,
                                    video=video_file,
                                    caption=f"Here's your Instagram video: {
                                        video_title}"
                                )
                                logger.info("Video sent successfully")

                                file_name = f"instagram_video_{
                                    message.from_user.id}.mp4"
                                doc_file = URLInputFile(
                                    video_url, filename=file_name)
                                await bot.send_document(
                                    chat_id=message.chat.id,
                                    document=doc_file,
                                    caption=f"Here's your Instagram video as a file: {
                                        video_title}",
                                    disable_content_type_detection=True
                                )
                                logger.info("Document sent successfully")
                            except Exception as send_error:
                                logger.error(
                                    f"Error sending video/document: {str(send_error)}")
                                await bot.send_message(message.chat.id, f"Error sending video/document: {str(send_error)}")
                        else:
                            await bot.send_message(message.chat.id, "This publication does not contain a video.")
                    else:
                        await bot.send_message(message.chat.id, f"API Error: {data.get('msg', 'Unknown error')}")
                else:
                    error_message = await response.text()
                    logger.error(f"API Error: HTTP {
                                 response.status}\nDetails: {error_message}")
                    await bot.send_message(message.chat.id, f"API Error: HTTP {response.status}\nDetails: {error_message}")
    except aiohttp.ClientError as client_error:
        logger.error(f"Network error: {str(client_error)}")
        await bot.send_message(message.chat.id, f"Network error: {str(client_error)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await bot.send_message(message.chat.id, f"Error while processing Instagram content: {str(e)}")

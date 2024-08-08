import json
import logging
import random

import aiohttp
from aiogram.types import URLInputFile

from config import RAPIDAPI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instagram(message, bot, instagram_url):
    try:
        async with aiohttp.ClientSession() as session:
            # Первый запрос к API Instagram Media Downloader
            async with session.get(
                "https://instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com/get-info-rapidapi",
                params={"url": instagram_url},
                headers={
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com"
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # logger.info(f"Full API response: {
                    #             json.dumps(data, indent=2)}")

                    if 'video' in data:
                        video_url = data['video']
                        logger.info(
                            f"Attempting to access video URL: {video_url}")

                        # Список User-Agent для рандомизации
                        user_agents = [
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
                        ]

                        # Дополнительные заголовки
                        headers = {
                            'User-Agent': random.choice(user_agents),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'DNT': '1',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Referer': 'https://www.instagram.com/'
                        }

                        # Посещаем главную страницу Instagram перед запросом видео
                        await session.get('https://www.instagram.com/', headers=headers)

                        # Запрос видео
                        async with session.head(video_url, headers=headers) as video_response:
                            # logger.info(f"Video response status: {
                            #             video_response.status}")
                            # logger.info(f"Video response headers: {
                            #             video_response.headers}")

                            if video_response.status == 200:
                                try:
                                    video_file = URLInputFile(video_url)
                                    await bot.send_video(
                                        chat_id=message.chat.id,
                                        video=video_file,
                                        caption="Here's your Instagram video"
                                    )
                                    logger.info("Video sent successfully")

                                    file_name = f"instagram_video_{
                                        message.from_user.id}.mp4"
                                    doc_file = URLInputFile(
                                        video_url, filename=file_name)
                                    await bot.send_document(
                                        chat_id=message.chat.id,
                                        document=doc_file,
                                        caption="Here's your Instagram video as a file",
                                        disable_content_type_detection=True
                                    )
                                    logger.info("Document sent successfully")
                                except Exception as send_error:
                                    logger.error(
                                        f"Error sending video/document: {str(send_error)}")
                                    await bot.send_message(message.chat.id, f"Error sending video/document: {str(send_error)}")
                            elif video_response.status == 403:
                                await bot.send_message(message.chat.id, "Access to the video is forbidden by Instagram. Please try again later or use a different link.")
                            else:
                                await bot.send_message(message.chat.id, f"Error accessing the video. Response code: {video_response.status}")
                    else:
                        await bot.send_message(message.chat.id, "This publication does not contain a video.")
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
        await bot.send_message(message.chat.id, f"Error while processing Instagram videos: {str(e)}")

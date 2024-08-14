import logging
import os
import shutil
import tempfile
import uuid

import ddinsta
from aiogram.types import FSInputFile

from config import BASE_DIR, TEMP_DIRECTORY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instagram(message, bot, instagram_url):
    # Generate a unique identifier for this request
    request_id = str(uuid.uuid4())
    temp_dir = os.path.join(TEMP_DIRECTORY, request_id)

    try:
        logger.info(f"Processing Instagram URL: {
                    instagram_url} for request {request_id}")

        # Create a unique temporary directory for this request
        os.makedirs(temp_dir, exist_ok=True)

        if "/reel/" in instagram_url:
            try:
                logger.info(f"Attempting to download video from: {
                            instagram_url}")
                result = ddinsta.save_video(instagram_url)
                logger.info(f"ddinsta.save_video result: {result}")

                if result == '[!] Success':
                    # Find the video file in the root directory
                    video_files = [f for f in os.listdir(
                        BASE_DIR) if f.endswith('.mp4')]
                    if not video_files:
                        raise FileNotFoundError(
                            "Video file not found in root directory")

                    original_video_path = os.path.join(
                        BASE_DIR, video_files[-1])
                elif os.path.exists(result):
                    original_video_path = result
                else:
                    raise FileNotFoundError(f"Video file not found: {result}")

                # Move the file to our temp directory
                video_path = os.path.join(temp_dir, f"video_{request_id}.mp4")
                shutil.move(original_video_path, video_path)
                logger.info(f"Moved video to: {video_path}")

                if os.path.getsize(video_path) == 0:
                    raise ValueError("Downloaded video file is empty")

                logger.info(f"Video file size: {
                            os.path.getsize(video_path)} bytes")

                # Send as video
                video_file = FSInputFile(video_path)
                await bot.send_video(chat_id=message.chat.id, video=video_file)

                # Send as document
                file_name = f"instagram_video_{message.from_user.id}.mp4"
                doc_file = FSInputFile(video_path, filename=file_name)
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=doc_file,
                    disable_content_type_detection=True
                )

                logger.info("Video successfully sent")
            except Exception as e:
                logger.error(
                    f"Error downloading or processing video: {str(e)}")
                await bot.send_message(message.chat.id, f"Error downloading video: {str(e)}")
        else:
            logger.warning(f"Invalid Instagram URL received: {instagram_url}")
            await bot.send_message(message.chat.id, "Invalid Instagram URL. Please provide a link to a reel.")

    except Exception as e:
        logger.error(f"Error processing Instagram video: {str(e)}")
        await bot.send_message(message.chat.id, f"Error processing Instagram video: {str(e)}")
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info(f"Cleaned up temporary directory for request {request_id}")

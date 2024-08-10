import asyncio
import logging
import os
import tempfile
import time
from pathlib import Path

import instaloader
from aiogram import Bot
from aiogram.types import FSInputFile
from instaloader.exceptions import ConnectionException, LoginRequiredException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting
RATE_LIMIT = 60  # seconds
last_request_time = 0


async def process_instagram(message, bot: Bot, instagram_url: str):
    global last_request_time

    # Check rate limit
    current_time = time.time()
    if current_time - last_request_time < RATE_LIMIT:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Please wait a moment before making another request. This helps us avoid overloading Instagram's servers."
        )
        return

    last_request_time = current_time

    try:
        # Extract the shortcode from the URL
        shortcode = instagram_url.split("/")[-2]

        # Initialize instaloader
        L = instaloader.Instaloader()

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                # Attempt to download the post without logging in
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=tmpdirname)

                # Find the video file
                video_file = next((f for f in os.listdir(
                    tmpdirname) if f.endswith('.mp4')), None)

                if video_file:
                    video_path = os.path.join(tmpdirname, video_file)
                    caption = post.caption if post.caption else 'Instagram video'

                    # Send as video
                    await bot.send_video(
                        chat_id=message.chat.id,
                        video=FSInputFile(video_path),
                        # Limit caption to 1024 characters
                        caption=caption[:1024]
                    )
                    logger.info(
                        f"Video sent successfully as video message: {video_file}")

                    # Send as document
                    await bot.send_document(
                        chat_id=message.chat.id,
                        document=FSInputFile(video_path),
                        caption=f"{caption[:1024]} (as document)",
                        disable_content_type_detection=True
                    )
                    logger.info(
                        f"Video sent successfully as document: {video_file}")
                else:
                    await bot.send_message(chat_id=message.chat.id, text="No video found in the Instagram post. This might be an image post or a private video.")

            except LoginRequiredException:
                logger.error("Login required to access this post")
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="This Instagram post is private or requires login to access. "
                         "I can only process public posts. Please try with a public Instagram post."
                )
            except ConnectionException as e:
                logger.error(f"Connection error: {str(e)}")
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="There was a connection error while trying to access Instagram. "
                         "This might be due to Instagram's rate limiting. Please try again later."
                )

    except instaloader.exceptions.InstaloaderException as e:
        logger.error(f"Instaloader error: {str(e)}")
        error_message = str(e)
        if "Checkpoint required" in error_message or "Please wait a few minutes" in error_message:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Instagram is currently limiting our access. This is a temporary issue. "
                     "Please try again later or use a different platform."
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text="There was an error processing your Instagram link. "
                     "Please make sure the post is public and try again later."
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

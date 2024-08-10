import asyncio
import logging
import os
import tempfile
from pathlib import Path

import instaloader
from aiogram import Bot
from aiogram.types import FSInputFile
from instaloader.exceptions import (
    BadCredentialsException,
    ConnectionException,
    LoginRequiredException,
    TwoFactorAuthRequiredException,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to store the session file
SESSION_FILE = Path("instagram_session")


async def login_to_instagram(L):
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        logger.warning(
            "Instagram credentials not set. Proceeding without login.")
        return False

    try:
        if SESSION_FILE.exists():
            L.load_session_from_file(username, str(SESSION_FILE))
            logger.info("Loaded session from file")
        else:
            L.login(username, password)
            L.save_session_to_file(str(SESSION_FILE))
            logger.info("Logged in and saved session to file")
        return True
    except TwoFactorAuthRequiredException:
        logger.error(
            "Two-factor authentication is required. Please set it up manually.")
        return False
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return False


async def process_instagram(message, bot: Bot, instagram_url: str):
    try:
        # Extract the shortcode from the URL
        shortcode = instagram_url.split("/")[-2]

        # Initialize instaloader
        L = instaloader.Instaloader()

        # Attempt to log in
        login_successful = await login_to_instagram(L)

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            try:
                # Download the post
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
                    await bot.send_message(chat_id=message.chat.id, text="No video found in the Instagram post.")

            except LoginRequiredException:
                logger.error("Login required to access this post")
                if not login_successful:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="This Instagram post requires login to access. The bot is currently unable to log in. Please try a public post or contact the bot administrator."
                    )
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text="This Instagram post requires login to access. Please try again later or contact the bot administrator."
                    )
            except ConnectionException as e:
                logger.error(f"Connection error: {str(e)}")
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="There was a connection error while trying to access Instagram. Please try again later."
                )

    except instaloader.exceptions.InstaloaderException as e:
        logger.error(f"Instaloader error: {str(e)}")
        error_message = str(e)
        if "Checkpoint required" in error_message:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Instagram has flagged the bot's account for a security check. The bot administrator needs to log in manually to resolve this issue. Please try again later."
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

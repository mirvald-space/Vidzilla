# Video Downloader Bot

This Telegram bot allows users to download videos from Instagram Reels and TikTok. It provides an easy way to save and share content from these popular social media platforms.

## Features

- Download videos from Instagram Reels and TikTok
- Receive videos as both video messages and downloadable files
- Simple and user-friendly interface

## Commands

- `/start` - Begin interaction with the bot and receive usage instructions
- `/help` - Get detailed information about the bot's functionality

## Installation and Setup

1. Clone this repository:

- git clone https://github.com/yourusername/video-downloader-bot.git
- cd video-downloader-bot

2. Install the required dependencies:

- pip install -r requirements.txt

3. Create a `.env` file in the project root and add the following environment variables:

- `BOT_TOKEN`: Your Telegram bot token obtained from BotFather
- `RAPIDAPI_KEY`: Your RapidAPI key for the Social Media Video Downloader API
- `WEBHOOK_PATH`: The path for your webhook (e.g., `/webhook`)
- `WEBHOOK_URL`: The full URL to your webhook (e.g., `https://your-domain.com/webhook`)

4. Set up a webhook for your bot on a server with HTTPS support.

5. Run the bot:
   python bot.py

## Usage

1. Start a chat with the bot on Telegram
2. Send the `/start` command to get instructions
3. Send a link to an Instagram Reel or TikTok video
4. The bot will process the link and send you the video as both a video message and a file

## Dependencies

- aiogram
- aiohttp
- python-dotenv

## API Used

This bot uses the Social Media Video Downloader API from RapidAPI to fetch video links.

## Note

Ensure you comply with the terms of service of Instagram and TikTok when using this bot.

## License

[MIT License](LICENSE)

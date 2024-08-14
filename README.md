# Social Media Video Downloader Bot

This Telegram bot allows users to download videos from various social media platforms including Instagram Reels, TikTok, YouTube, Facebook, Twitter, and Pinterest. It provides an easy way to save and share content from these popular social media platforms.

## Features

- Download videos from Instagram Reels, TikTok, YouTube, Facebook, Twitter, and Pinterest
- Receive videos as both video messages and downloadable files
- User management system with free and premium tiers
- Admin functionality for generating coupons and viewing usage statistics
- Simple and user-friendly interface

## Commands

- `/start` - Begin interaction with the bot and receive usage instructions
- `/help` - Get detailed information about the bot's functionality
- `/activate_coupon` - Activate a coupon code for premium access

### Admin Commands

- `/generate_coupon` - Generate a new coupon (admin only)
- `/stats` - View usage statistics (admin only)

## Installation and Setup

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/social-media-video-downloader-bot.git
   cd social-media-video-downloader-bot
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add the following environment variables:

   - `BOT_TOKEN`: Your Telegram bot token obtained from BotFather
   - `RAPIDAPI_KEY`: Your RapidAPI key for the Social Media Video Downloader API
   - `WEBHOOK_PATH`: The path for your webhook (e.g., `/webhook`)
   - `WEBHOOK_URL`: The full URL to your webhook (e.g., `https://your-domain.com/webhook`)
   - `MONGODB_URI`: Your MongoDB connection string
   - `MONGODB_DB_NAME`: Name of your MongoDB database
   - `MONGODB_USERS_COLLECTION`: Name of the collection for user data
   - `MONGODB_COUPONS_COLLECTION`: Name of the collection for coupon data
   - `ADMIN_IDS`: Comma-separated list of admin user IDs
   - `FREE_LIMIT`: Number of free downloads allowed per user (default is 3)

4. Set up a webhook for your bot on a server with HTTPS support.

5. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Start a chat with the bot on Telegram
2. Send the `/start` command to get instructions
3. Send a link to a video from any supported platform (Instagram, TikTok, YouTube, Facebook, Twitter, or Pinterest)
4. The bot will process the link and send you the video as both a video message and a file

### Premium Access

Users have a limited number of free downloads. To get unlimited access:

1. Obtain a coupon code from an admin
2. Use the `/activate_coupon` command and enter the coupon code

## Admin Functionality

Admins can perform the following actions:

- Generate coupon codes for premium access using `/generate_coupon`
- View usage statistics including total users, active subscriptions, total downloads, and unused coupons using `/stats`

## Dependencies

- aiogram
- aiohttp
- python-dotenv
- pymongo
- requests
- ddinsta (for Instagram video downloads)

## API Used

This bot uses the Social Media Video Downloader API from RapidAPI to fetch video links from various platforms.

## Note

Ensure you comply with the terms of service of all supported platforms when using this bot.

## License

[MIT License](LICENSE)

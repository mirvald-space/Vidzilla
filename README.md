# Social Media Video Downloader Bot

Easily download and share videos from your favorite social media platforms with our Telegram bot! Whether it's Instagram Reels, TikTok, YouTube, Facebook, Twitter, or Pinterest, this bot has got you covered. Perfect for those who want to save content for offline viewing or reposting.

🎥 **Save videos from multiple platforms in a snap!**
🚀 **Simple, fast, and user-friendly!**

## Features

- Download videos from Instagram Reels, TikTok, YouTube, Facebook, Twitter, and Pinterest
- Receive videos as both video messages and downloadable files
- User management system with free and premium tiers
- Stripe integration for subscription payments
- Admin functionality for generating coupons and viewing usage statistics
- Simple and user-friendly interface

## Supported Platforms

| Platform  | Status |
| --------- | ------ |
| Instagram | ✅     |
| TikTok    | ✅     |
| YouTube   | ✅     |
| Facebook  | ✅     |
| Twitter   | ✅     |
| Pinterest | ✅     |

## Commands

- `/start` - Begin interaction with the bot and receive usage instructions
- `/help` - Get detailed information about the bot's functionality
- `/subscribe` - View and select subscription plans

### Admin Commands

- `/generate_coupon` - Generate a new coupon (admin only)
- `/stats` - View usage statistics (admin only)

## Subscription Plans

- 1 month subscription
- 3 months subscription
- Lifetime subscription

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
- `BOT_USERNAME`: Your Telegram bot's username (without @)
- `RAPIDAPI_KEY`: Your RapidAPI key for the Social Media Video Downloader API
- `WEBHOOK_PATH`: The path for your webhook (e.g., `/webhook`)
- `WEBHOOK_URL`: The full URL to your webhook (e.g., `https://your-domain.com/webhook`)
- `MONGODB_URI`: Your MongoDB connection string
- `MONGODB_DB_NAME`: Name of your MongoDB database
- `MONGODB_USERS_COLLECTION`: Name of the collection for user data
- `MONGODB_COUPONS_COLLECTION`: Name of the collection for coupon data
- `ADMIN_IDS`: Comma-separated list of admin user IDs
- `FREE_LIMIT`: Number of free downloads allowed per user (default is 3)
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key
- `STRIPE_WEBHOOK_SECRET`: Your Stripe webhook secret
- `STRIPE_SUCCESS_URL`: URL to redirect after successful payment (default is https://t.me/your_bot_username)
- `STRIPE_CANCEL_URL`: URL to redirect after cancelled payment (default is https://t.me/your_bot_username)

4. Set up a webhook for your bot on a server with HTTPS support.

5. Run the bot:
   ```
   python bot.py
   ```

## Stripe Integration

This bot uses Stripe for handling payments. It supports both credit card payments and PayPal.

To set up Stripe for production payments:

1. Create a Stripe account at https://stripe.com if you haven't already.
2. In the Stripe Dashboard, navigate to the API keys section.
3. Copy your live secret key and publishable key.
4. Update your `.env` file with these live keys:
   ```
   STRIPE_SECRET_KEY=your_live_secret_key
   STRIPE_PUBLISHABLE_KEY=your_live_publishable_key
   ```
5. Set up a webhook in the Stripe Dashboard:
   - Go to Developers > Webhooks
   - Add a new endpoint with your production URL
   - Select the events you want to listen for (at minimum, `checkout.session.completed`)
   - Copy the webhook signing secret and add it to your `.env` file:
     ```
     STRIPE_WEBHOOK_SECRET=your_webhook_signing_secret
     ```
6. To enable PayPal:
   - In the Stripe Dashboard, go to Settings > Payment methods
   - Find PayPal in the list and click 'Set up'
   - Follow the instructions to connect your PayPal account
7. Update the success and cancel URLs in `config.py` to point to your production bot's URL.
8. Test the integration thoroughly in Stripe's test mode before switching to live mode.

Remember to keep your Stripe API keys and webhook secret secure and never expose them publicly.

## Usage

1. Start a chat with the bot on Telegram
2. Send the `/start` command to get instructions
3. Send a link to a video from any supported platform
4. The bot will process the link and send you the video as both a video message and a file
5. Use `/subscribe` to view and purchase subscription plans

### Premium Access

Users have a limited number of free downloads. To get unlimited access:

1. Use the `/subscribe` command to view available plans
2. Select a plan to proceed to payment
3. Complete the payment process through Stripe
4. Once payment is confirmed, the subscription will be automatically activated

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
- stripe

## API Used

This bot uses the Social Media Video Downloader API from RapidAPI to fetch video links from various platforms.

## Note

Ensure you comply with the terms of service of all supported platforms when using this bot.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for details on how to get started.

## License

[MIT License](LICENSE)

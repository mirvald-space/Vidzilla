# handlers.py

import re

from aiogram import Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from handlers import facebook, instagram, pinterest, tiktok, twitter, youtube
from utils.user_management import (
    activate_coupon,
    check_user_limit,
    create_coupon,
    get_limit_exceeded_message,
    get_usage_stats,
    handle_coupon_activation,
    is_admin,
)


class DownloadVideo(StatesGroup):
    waiting_for_link = State()
    waiting_for_coupon = State()


class AdminActions(StatesGroup):
    waiting_for_coupon_duration = State()


async def send_welcome(message: Message, state: FSMContext):
    await message.answer("<b>👋 Hi!\n I can download videos from Instagram Reels, TikTok, YouTube, and Facebook.</b>\n\n"
                         "<b>Available commands:</b>\n\n"
                         "/start - start working with the bot\n"
                         "/help - get help\n"
                         "/activate_coupon - activate a coupon code\n\n"
                         "Just send me a video link, and I'll return it as a video message and a file.",
                         parse_mode="HTML")
    await state.set_state(DownloadVideo.waiting_for_link)


async def send_help(message: Message):
    help_text = ("This bot helps download videos from Instagram Reels, TikTok, YouTube, and Facebook.\n\n"
                 "How to use:\n"
                 "1. Send the bot a link to a video.\n"
                 "2. The bot will process the link and return the video in two formats:\n"
                 "   - As a video message\n"
                 "   - As a document file\n\n"
                 "Supported services:\n"
                 "- Instagram Reels\n"
                 "- TikTok\n"
                 "- YouTube\n"
                 "- Facebook\n\n"
                 "Commands:\n"
                 "/start - start working with the bot\n"
                 "/help - show this help message\n"
                 "/activate_coupon - activate a coupon code")

    if is_admin(message.from_user.id):
        help_text += ("\n\nAdmin commands:\n"
                      "/generate_coupon - generate a new coupon\n"
                      "/stats - view usage statistics")

    await message.answer(help_text)


async def process_link(message: Message, state: FSMContext, bot: Bot):
    url = message.text
    if not check_user_limit(message.from_user.id):
        await message.answer(get_limit_exceeded_message())
        return

    await message.answer("Processing your link...")
    try:
        if 'instagram.com' in url:
            await instagram.process_instagram(message, bot, url)
        elif 'tiktok.com' in url:
            await tiktok.process_tiktok(message, bot, url)
        elif 'x.com' in url:
            await twitter.process_twitter(message, bot, url)
        elif 'youtube.com' in url or 'youtu.be' in url:
            await youtube.process_youtube(message, bot, url)
        elif 'facebook.com' in url:
            await facebook.process_facebook(message, bot, url)
        elif 'pin.it' in url:
            await pinterest.process_pinterest(message, bot, url)
        else:
            await message.answer("Unsupported platform. Please provide a link from Instagram, TikTok, YouTube, or Facebook.")
    except Exception as e:
        await message.answer(f"Error processing video: {str(e)}")

    await state.clear()
    await state.set_state(DownloadVideo.waiting_for_link)


async def activate_coupon_command(message: Message, state: FSMContext):
    await message.answer("Please enter your coupon code:")
    await state.set_state(DownloadVideo.waiting_for_coupon)


async def handle_coupon_activation(message: Message, state: FSMContext):
    coupon_code = message.text.strip()
    activation_result = activate_coupon(message.from_user.id, coupon_code)

    if activation_result:
        await message.answer("Coupon successfully activated! Now you have access to the bot!")
        # Change state back to waiting for link
        await state.set_state(DownloadVideo.waiting_for_link)
    else:
        await message.answer("Invalid or already used coupon code. Please try again or contact the admin.")


async def generate_coupon_command(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("This command is only available for admins.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 month", callback_data="coupon_1month")],
        [InlineKeyboardButton(
            text="3 months", callback_data="coupon_3months")],
        [InlineKeyboardButton(
            text="Lifetime", callback_data="coupon_lifetime")]
    ])

    await message.answer("Please choose the coupon duration:", reply_markup=keyboard)
    await state.set_state(AdminActions.waiting_for_coupon_duration)


async def handle_coupon_generation(callback_query: CallbackQuery, state: FSMContext):
    duration_map = {
        'coupon_1month': '1month',
        'coupon_3months': '3months',
        'coupon_lifetime': 'lifetime'
    }
    duration = duration_map.get(callback_query.data)

    if not duration:
        await callback_query.message.answer("Invalid duration. Please use the provided buttons.")
        return

    coupon_code = create_coupon(duration)

    # Send success message
    await callback_query.message.answer("Coupon generated successfully!")

    # Send coupon code in a separate message
    await callback_query.message.answer(f"`{coupon_code}`", parse_mode="Markdown")

    await callback_query.answer()
    await state.clear()


async def stats_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("This command is only available for admins.")
        return

    stats = get_usage_stats()
    stats_message = (f"Usage Statistics:\n\n"
                     f"Total Users: {stats['total_users']}\n"
                     f"Active Subscriptions: {stats['active_subscriptions']}\n"
                     f"Total Downloads: {stats['total_downloads']}\n"
                     f"Unused Coupons: {stats['unused_coupons']}")
    await message.answer(stats_message)


def register_handlers(dp):
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(send_help, Command(commands=['help']))
    dp.message.register(activate_coupon_command,
                        Command(commands=['activate_coupon']))
    dp.message.register(generate_coupon_command,
                        Command(commands=['generate_coupon']))
    dp.message.register(stats_command, Command(commands=['stats']))
    dp.message.register(process_link, DownloadVideo.waiting_for_link)
    dp.message.register(handle_coupon_activation,
                        DownloadVideo.waiting_for_coupon)
    dp.callback_query.register(
        handle_coupon_generation, AdminActions.waiting_for_coupon_duration)

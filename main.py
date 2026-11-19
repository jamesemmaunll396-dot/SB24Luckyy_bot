import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "សូមស្វាគមន៍មកវេបសាយធំបំផុត ងាយស្រួលលេង📲 "
    "និងគួរឱ្យទុកចិត្តបំផុតនៅកម្ពុជា🔥សេវាកម្ម២៤ម៉ោង: "
    "https://t.me/Sdrservice24h"
)


def build_welcome_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("ទាក់ទងសេវាកម្ម 24h", url="https://t.me/Sdrservice24h")],
        [InlineKeyboardButton("ព័ត៌មានបន្ថែម", callback_data="more_info")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=build_welcome_keyboard(),
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    # Always answer callback queries promptly so Telegram stops the loading spinner
    await query.answer()

    if query.data == "more_info":
        await query.message.reply_text(
            "សូមចុចតំណភ្ជាប់ខាងលើ ដើម្បីទាក់ទងសេវាកម្ម ២៤ម៉ោង: https://t.me/Sdrservice24h"
        )


async def echo_or_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=build_welcome_keyboard(),
    )


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable.")

    logger.info("Starting Telegram bot...")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_or_reply))

    logger.info("Bot is ready to receive Telegram messages.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from datetime import datetime
from zoneinfo import ZoneInfo
import random

TOKEN = "8631765317:AAFmdSUxg7WuCJQHUeRPReaA7yH2HbR8D34"


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("🎲 Random Number", callback_data="random")],
        [InlineKeyboardButton("🇬🇧 London Time", callback_data="time")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Welcome!\nChoose an option:",
        reply_markup=reply_markup
    )


# ---------- COMMANDS ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - menu\n"
        "/help - help\n"
        "/roll - random number\n"
        "/time - London time"
    )


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 100)
    await update.message.reply_text(f"🎲 Number: {number}")


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    london_time = datetime.now(
        ZoneInfo("Europe/London")
    ).strftime("%H:%M:%S")

    await update.message.reply_text(f"🇬🇧 London: {london_time}")


# ---------- BUTTONS ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "🤖 Simple Telegram Bot\nCreated with Python."
        )

    elif query.data == "random":
        number = random.randint(1, 100)
        await query.message.reply_text(f"🎲 Number: {number}")

    elif query.data == "time":
        london_time = datetime.now(
            ZoneInfo("Europe/London")
        ).strftime("%H:%M:%S")

        await query.message.reply_text(f"🇬🇧 London: {london_time}")

    elif query.data == "help":
        await query.message.reply_text("Use /start to open menu")


# ---------- ECHO ----------
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            f"You said: {update.message.text}"
        )


# ---------- APP ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("roll", roll))
app.add_handler(CommandHandler("time", time_command))

app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Bot is running")
app.run_polling(drop_pending_updates=True)

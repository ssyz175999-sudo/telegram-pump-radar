import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 رادار پامپ اسپات فعال شد!\n"
        "در حال آماده‌سازی پایش بازار..."
    )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Spot Pump Radar is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 رادار پامپ فعال شد!\n"
        "برای دریافت وضعیت رادار آماده‌ام."
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

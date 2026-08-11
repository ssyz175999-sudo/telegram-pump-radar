import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def get_market():
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false",
    }

    response = requests.get(COINGECKO_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 رادار اسپات فعال شد.\n"
        "در حال بررسی بازار..."
    )


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        coins = get_market()

        if not coins:
            await update.message.reply_text("⚠️ داده بازار دریافت نشد.")
            return

        top = coins[:10]

        lines = ["📊 وضعیت بازار اسپات\n"]

        for coin in top:
            name = coin.get("symbol", "").upper()
            price_change = coin.get("price_change_percentage_24h")

            if price_change is None:
                price_change = 0

            lines.append(
                f"{name}: {price_change:+.2f}%"
            )

        await update.message.reply_text("\n".join(lines))

    except Exception as error:
        print(f"Market error: {error}")
        await update.message.reply_text(
            "⚠️ دریافت داده بازار با خطا مواجه شد."
        )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("market", market))

    print("Spot Radar is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

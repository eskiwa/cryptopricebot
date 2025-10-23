import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from datetime import datetime
import traceback
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CMC_API_KEY = os.getenv("CMC_API_KEY")

data = ''
coin = ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global coin
    user = update.message.from_user
    coin = update.message.text  # Save to variable
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"📩 [{timestamp}]\nUser: @{user.username} ({user.id})\nMessage: {coin}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=log_message)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': f'{coin.upper()}',   # You can change this to ETH, SOL, etc.
        'convert': 'USD'
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    message = f"${data['data'][coin.upper()]['quote']['USD']['price']}"
    if message == "$None":
        await update.message.reply_text("Invalid coin")
    else:
        price = float(f"{data['data'][coin.upper()]['quote']['USD']['price']}")
        if price > 1000:
            await update.message.reply_text(f"${price:.2f}")
        elif price > 100:
            await update.message.reply_text(f"${price:.4f}")
        else:
            await update.message.reply_text(f"${price:.10f}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("⚠️ An error occurred:")
    print(traceback.format_exc())  # full traceback in Render logs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I’m xereabot 🤖\nChat the name of the coin to use the bot\nExample:\nBTC\nSOL\nETH")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("start", start))
app.add_error_handler(error_handler)
app.run_polling()
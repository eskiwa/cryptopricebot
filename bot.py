import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime
import traceback

data = ''
bot_token = "8414940488:AAEDjdVdRKpHqLGuVX-QEjVrXJZ8oMp4QhM"
coin = ""
ADMIN_ID = 8250762387

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
    'X-CMC_PRO_API_KEY': '3ba60acd46b94e928189c6a5155612f8',
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

app = ApplicationBuilder().token(bot_token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_error_handler(error_handler)
app.run_polling()
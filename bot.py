import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

data = ''
###
# symbol = input("coin")

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# parameters = {
#         'symbol': f'{symbol.upper()}',   # You can change this to ETH, SOL, etc.
#         'convert': 'USD'
# }

# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': '3ba60acd46b94e928189c6a5155612f8',
# }

# session = requests.Session()
# session.headers.update(headers)

# try:
#     response = session.get(url, params=parameters)
#     data = json.loads(response.text)
#     print(f"${data['data'][symbol.upper()]['quote']['USD']['price']}")
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)

############################################################################################################

bot_token = "8414940488:AAEDjdVdRKpHqLGuVX-QEjVrXJZ8oMp4QhM"
# chat_id = "8250762387"
# #message = f"${data['data'][symbol.upper()]['quote']['USD']['price']}"

# boturl = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# payload = {
#     "chat_id": chat_id,
#     "text": message
# }

# response = requests.post(boturl, data=payload)

# if response.status_code == 200:
#     print("Message sent successfully!")
# else:
#     print("Failed to send message:", response.text)



coin = ""


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global coin
    coin = update.message.text  # Save to variable

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

app = ApplicationBuilder().token(bot_token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
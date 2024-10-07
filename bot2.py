import openai
import ccxt
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext
import re
import asyncio
from telethon import TelegramClient, events
import requests
import time

# Personal API keys and secrets - you need to replace these with your own
openai_api_key = "your-openai-api-key"
api_id = "your-telegram-api-id"
api_hash = "your-telegram-api-hash"
phone_number = "your-phone-number"
binance_api_key = "your-binance-api-key"
binance_secret_key = "your-binance-secret-key"

# Parameters for trading (adjust them as you like)
stop_loss_percentage = 1.2
take_profit_percentage = 0.95
amount_to_trade = 10000

# Cryptocurrencies we don't want to trade
disallowed_symbols = ["BTC", "ETH", "XRP", "BNB", "ADA", "SOL"]

# Set up OpenAI and Binance clients
openai.api_key = openai_api_key
binance = ccxt.binanceusdm({
    'apiKey': binance_api_key,
    'secret': binance_secret_key,
    'enableRateLimit': False,
})

# Function to send a message to ChatGPT and get a response
def get_chat_gpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json",
    }
    conversation_history = [
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    data = {
        "model": "gpt-3.5-turbo-0301", 
        "messages": conversation_history,
        "max_tokens": 24,
        "temperature": 0.1, 
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()

    generated_text = ""
    for message in response_json['choices'][0]['message']:
        if message['role'] == "assistant":
            generated_text = message['content'].strip()
            break

    return generated_text

# Function to parse the ChatGPT response into usable data
def parse_gpt_response(response):
    call_pattern = re.compile(r'CALL:\\s*(NEW|OLD)')
    direction_pattern = re.compile(r'DIRECTION:\\s*(BUY|SELL)')
    pair_pattern = re.compile(r'PAIR:\\s*([A-Z]+)')

    call_status_match = call_pattern.search(response)
    direction_match = direction_pattern.search(response)
    crypto_name_match = pair_pattern.search(response)

    call_status = call_status_match.group(1) if call_status_match else "Not sure"
    direction = direction_match.group(1) if direction_match else "Not sure"
    crypto_name = crypto_name_match.group(1) if crypto_name_match else "Not sure"

    if "Not sure" in [call_status, direction, crypto_name]:
        return None

    return call_status, direction, crypto_name

# Function to analyze the incoming Telegram message and extract trading info
def analyze_message(message):
    prompt = (
        "I will give you an exact trading signal, followed by an image "
        "which you will not receive. I want you to specify if it's a new call or an update "
        "of a previous call (usually when it's BTC), direction (buy or sell), and the cryptocurrency. "
        "Respond in this format: "
        "\"CALL: NEW/OLD, DIRECTION: BUY/SELL, PAIR: CRYPTONAME\". "
        "This is the call: "
    )

    full_prompt = prompt + message
    analysis = get_chat_gpt_response(full_prompt)
    return parse_gpt_response(analysis)

# Executes a trade on Binance with the specified parameters
def execute_trade(symbol, direction):
    symbol = f"{symbol}USDT"
    place_order(symbol, direction, stop_loss_percentage, take_profit_percentage)

# Function to place a market order with stop loss and take profit on Binance
def place_order(symbol, direction, stop_loss_percentage, take_profit_percentage):
    side = 'buy' if direction == 'buy' else 'sell'
    opposite_side = 'sell' if side == 'buy' else 'buy'

    ticker = binance.fetch_ticker(symbol)
    ticker_price = float(ticker['last'])
    amount = amount_to_trade / ticker_price

    try:
        order = binance.create_order(symbol, 'market', side, amount)
        entry_price = float(order['price'])
        stop_loss_price = entry_price * (1 - stop_loss_percentage / 100) if direction == 'buy' else entry_price * (1 + stop_loss_percentage / 100)
        take_profit_price = entry_price * (1 + take_profit_percentage / 100) if direction == 'buy' else entry_price * (1 - take_profit_percentage / 100)
        partial_take_profit_price = entry_price * (1 + take_profit_percentage / 200) if direction == 'buy' else entry_price * (1 - take_profit_percentage / 200)

        # Place stop loss and take profit orders
        binance.create_order(symbol, 'STOP_MARKET', opposite_side, amount, None, {'stopPrice': stop_loss_price})
        binance.create_order(symbol, 'TAKE_PROFIT_MARKET', opposite_side, amount * 0.7, None, {'stopPrice': take_profit_price})
        binance.create_order(symbol, 'TAKE_PROFIT_MARKET', opposite_side, amount * 0.3, None, {'stopPrice': partial_take_profit_price})

    except Exception as e:
        print(f"Error placing order: {e}")

# Handles incoming Telegram messages
def handle_message(update, context):
    message_text = update.message.text
    extracted_info = analyze_message(message_text)

    if not extracted_info:
        print("Couldn't analyze the message")
        return

    is_new_call = extracted_info['is_new_call']
    direction = extracted_info['direction']
    symbol = extracted_info['symbol']

    if symbol in disallowed_symbols:
        print(f"Skipping trade for {symbol}")
        return

    if is_new_call:
        execute_trade(symbol, direction)

# Main function for running the Telegram client and listening to messages
async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()
    await client.send_code_request(phone_number)
    code = input('Enter the authorization code: ')
    await client.sign_in(phone_number, code)

    @client.on(events.NewMessage)
    async def my_event_handler(event):
        update = Update(event.message.id, message=event.message)
        handle_message(update, None)

    await client.run_until_disconnected()

asyncio.run(main())

Automated Trading Bot - Telegram & Binance Integration

Here's something cool I wanted to share. I created a trading bot that's a bit different from what you usually see. It was inspired by the activity in TraderSZ's Telegram group, which is packed with over 80,000 members.
I noticed that when TraderSZ mentions an altcoin, there's a significant swing in its price due to the buy/sell pressure from his followers. So, I set up my bot to automatically read and classify these calls - long or short, new or an update.
What's more, my bot smartly ignores larger, less impactable cryptos like BTC, ETH, or BNB, and doesn't pay attention to TraderSZ's take profit or stop loss levels either. The goal here is to catch the initial surge or drop triggered by the massive community, not the eventual targets set by TraderSZ.


Key Features
Automatically detects trading signals from a Telegram channel.
Classifies trades as long or short, new or update using AI.
Ignores larger cryptocurrencies like BTC, ETH, and BNB.
Executes trades on Binance with stop-loss and take-profit strategies.
Runs on OpenAI's GPT-3.5 to analyze messages from Telegram.
Getting Started
Prerequisites
Python 3.x
Binance account with API access.
Telegram bot and API access.
OpenAI API key for GPT-3.5.
Installation
Download the bot file:

Ensure you have bot2.py in your local directory.
Set Up a Virtual Environment (Optional but recommended):


python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
Install Dependencies: You need to install the required libraries. Run the following command in the directory where bot2.py is located:


pip install openai ccxt telethon requests python-telegram-bot
API Setup
OpenAI API Key
Sign up at OpenAI and get your API key.

In the bot2.py file, replace the placeholder with your API key:


openai_api_key = "your-openai-api-key"
Binance API Key
Create an account at Binance and generate API keys.

Replace the placeholders in the bot2.py file:


binance_api_key = "your-binance-api-key"
binance_secret_key = "your-binance-secret-key"
Telegram API Key
Talk to BotFather to create a new bot and get your bot token.

Go to my.telegram.org and generate your api_id and api_hash.

Replace the placeholders in the bot2.py file:

api_id = "your-telegram-api-id"
api_hash = "your-telegram-api-hash"
phone_number = "your-phone-number"
Configuration
You can modify the following parameters in bot2.py to match your trading preferences:

stop_loss_percentage: Set your stop loss percentage.
take_profit_percentage: Set your take profit percentage.
amount_to_trade: Define how much you wish to trade on each signal.
disallowed_symbols: Specify cryptocurrencies you want to ignore (e.g., BTC, ETH, BNB).
Running the Bot
To run the bot, execute the following command in your terminal:


python bot2.py
The bot will start by connecting to Telegram and Binance. The first time you run it, you will need to authenticate it with Telegram using the code sent to your phone.

How It Works
The bot listens for messages in the specified Telegram group.
It uses OpenAI GPT-3.5 to analyze and classify signals as long/short and new/update.
It places buy/sell orders on Binance with stop-loss and take-profit levels.
Disclaimer
Please note that while this bot has been tested, cryptocurrency trading carries risk. Always trade responsibly and manage your risks effectively.


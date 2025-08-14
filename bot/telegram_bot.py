import os
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# 🔹 Watchlist (in-memory; replace with DB for persistence)
watchlist = set()

# 🔹 Dynamic asset type detection
def detect_asset_type(ticker):
    # Replace with your own logic or metadata lookup
    return "crypto" if ticker.upper().endswith("USD") or ticker.upper().startswith("BTC") else "stock"

# 🔹 Alert Formatter
def format_alert(data):
    return f"""
🚨 Signal Alert: ${data['ticker']} ({data['type'].capitalize()})

📈 Price: ${data['price']} ({data['change']}%)
📊 AI Score: {data['ai_score']}/10 ✅ {data['confidence']}
🧠 Reason: \"{data['narrative']}\"
📡 Sentiment: {data['sentiment']}
📰 Catalyst: {data['catalyst']}

📍 Risk Panel:
- Stop Loss: ${data['stop_loss']}
- Take Profit: ${data['take_profit']}
- Position Size: ${data['position_size']}

📅 Time: {data['timestamp']}
🔗 [Chart View]({data['chart_url']})
🔗 [News Source]({data['news_url']})
🔗 [Tweet]({data['tweet_url']})
"""

# 🔹 Telegram Alert Sender
def send_telegram_alert(signal):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    crypto_chat_id = os.getenv("TELEGRAM_CHAT_ID_CRYPTO")
    stocks_chat_id = os.getenv("TELEGRAM_CHAT_ID_STOCKS")

    chat_id = crypto_chat_id if signal.get("type") == "crypto" else stocks_chat_id
    message = format_alert(signal)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add", callback_data=f"add_{signal['ticker']}"),
         InlineKeyboardButton("❌ Remove", callback_data=f"remove_{signal['ticker']}")],
        [InlineKeyboardButton("📋 Watchlist", callback_data="watchlist")]
    ])

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": keyboard.to_json()
        }
    )

# 🔹 Dispatcher
def dispatch_alerts(signals):
    for signal in signals:
        if (
            signal["ai_score"] >= 7
            and signal["confidence"] in ["High", "Medium"]
            and signal.get("sentiment", "").lower() == "bullish"
        ):
            signal["type"] = detect_asset_type(signal["ticker"])
            send_telegram_alert(signal)

# 🔹 /scan command
def handle_scan_command(update: Update, context: CallbackContext):
    if context.args:
        ticker = context.args[0].upper()
        update.message.reply_text(f"🔍 Scanning {ticker}...")

        try:
            raw_signal = scan_single_asset(ticker)
            enriched = enrich_signal(raw_signal)
            enriched["type"] = detect_asset_type(ticker)
            send_telegram_alert(enriched)
        except Exception as e:
            update.message.reply_text(f"⚠️ Error scanning {ticker}: {str(e)}")
    else:
        update.message.reply_text("📡 Running full scan...")
        try:
            signals = run_all_scans()
            enriched_signals = enrich_signals(signals)
            top_signals = [
                s for s in enriched_signals
                if s["ai_score"] >= 7 and s["confidence"] in ["High", "Medium"] and s.get("sentiment") == "bullish"
            ][:3]

            if not top_signals:
                update.message.reply_text("⚠️ No strong signals found right now.")
                return

            dispatch_alerts(top_signals)
        except Exception as e:
            update.message.reply_text(f"⚠️ Scan failed: {str(e)}")

# 🔹 Watchlist Commands
def handle_add(update: Update, context: CallbackContext):
    if context.args:
        ticker = context.args[0].upper()
        watchlist.add(ticker)
        update.message.reply_text(f"✅ {ticker} added to watchlist.")
    else:
        update.message.reply_text("Usage: /add BTC")

def handle_remove(update: Update, context: CallbackContext):
    if context.args:
        ticker = context.args[0].upper()
        watchlist.discard(ticker)
        update.message.reply_text(f"❌ {ticker} removed from watchlist.")
    else:
        update.message.reply_text("Usage: /remove BTC")

def handle_watchlist(update: Update, context: CallbackContext):
    if not watchlist:
        update.message.reply_text("📋 Watchlist is empty.")
    else:
        update.message.reply_text("📋 Watchlist:\n" + "\n".join(sorted(watchlist)))

# 🔹 Inline Button Handler
def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data.startswith("add_"):
        ticker = query.data.split("_")[1]
        watchlist.add(ticker)
        query.edit_message_reply_markup(None)
        query.message.reply_text(f"✅ {ticker} added to watchlist.")
    elif query.data.startswith("remove_"):
        ticker = query.data.split("_")[1]
        watchlist.discard(ticker)
        query.edit_message_reply_markup(None)
        query.message.reply_text(f"❌ {ticker} removed from watchlist.")
    elif query.data == "watchlist":
        handle_watchlist(query, context)

# 🔹 Bot Setup
def start_bot():
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("scan", handle_scan_command))
    dispatcher.add_handler(CommandHandler("add", handle_add))
    dispatcher.add_handler(CommandHandler("remove", handle_remove))
    dispatcher.add_handler(CommandHandler("watchlist", handle_watchlist))
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()

# 🔹 Entry Point
if __name__ == "__main__":
    start_bot()

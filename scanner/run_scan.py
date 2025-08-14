from dotenv import load_dotenv
from scanner.stock_scanner import scan_stocks
from scanner.crypto_scanner import scan_crypto
from utils.alert_formatter import format_alert
from utils.telegram_alert import send_telegram_alert

load_dotenv()

def run_scanner():
    print("🔍 Running full asset scanner...")

    # Scan both asset classes
    stock_signals = scan_stocks()
    crypto_signals = scan_crypto()

    all_signals = stock_signals + crypto_signals

    for signal in all_signals:
        alert_text = format_alert(signal)
        send_telegram_alert(alert_text, signal["type"])

    print(f"✅ Sent {len(all_signals)} alerts.")

if __name__ == "__main__":
    run_scanner()

from flask import Flask, render_template, redirect, session, request
from scanner.crypto_scanner import fetch_crypto_signals
from scanner.stock_scanner import fetch_stock_signals
from scanner.enrich_signal import enrich_signals
from alerts.telegram_alert import send_telegram_alert
from watchlist.watchlist_manager import (
    load_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
    filter_signals_by_watchlist
)
from auth.auth_routes import auth_bp
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(auth_bp)

@app.route("/")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    crypto_signals = fetch_crypto_signals()
    stock_signals = fetch_stock_signals()

    enriched_crypto = enrich_signals(crypto_signals)
    enriched_stock = enrich_signals(stock_signals)

    watchlist_signals = filter_signals_by_watchlist(enriched_crypto + enriched_stock)

    for signal in enriched_crypto + enriched_stock:
        if signal["score"] > 7:
            send_telegram_alert(signal)

    return render_template(
        "index.html",
        crypto=enriched_crypto,
        stocks=enriched_stock,
        watchlist=watchlist_signals
    )

@app.route("/watchlist")
def view_watchlist():
    if "user" not in session:
        return redirect("/login")
    tickers = load_watchlist()
    return render_template("watchlist.html", watchlist=tickers)

@app.route("/watchlist/add/<ticker>", methods=["POST"])
def add_watch(ticker):
    if "user" not in session:
        return "Unauthorized", 401
    add_to_watchlist(ticker)
    return "OK"

@app.route("/watchlist/remove/<ticker>", methods=["POST"])
def remove_watch(ticker):
    if "user" not in session:
        return redirect("/login")
    remove_from_watchlist(ticker)
    return redirect("/watchlist")

if __name__ == "__main__":
    app.run(debug=False)

from flask import Blueprint, jsonify, request
from watchlist.watchlist_manager import load_watchlist, save_watchlist

bp = Blueprint("watchlist_api", __name__)

@bp.route("/api/watchlist")
def get_watchlist():
    return jsonify(load_watchlist())

@bp.route("/api/watchlist/remove/<ticker>", methods=["POST"])
def remove_watchlist_item(ticker):
    watchlist = load_watchlist()
    updated = [item for item in watchlist if item["ticker"].lower() != ticker.lower()]
    save_watchlist(updated)
    return jsonify({"status": "removed", "ticker": ticker})

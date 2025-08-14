import requests

def enrich_with_reddit(signals):
    """
    Enrich each signal with Reddit thread metadata.

    Args:
        signals (list): List of signal dictionaries with 'ticker' or 'name'

    Returns:
        list: Signals enriched with Reddit summary
    """
    if not signals:
        print("[Reddit] No signals provided.")
        return []

    enriched = []
    for signal in signals:
        query = signal.get("name") or signal.get("ticker")
        reddit_data = fetch_reddit_summary(query)
        signal["reddit_summary"] = reddit_data
        enriched.append(signal)

    return enriched


def fetch_reddit_summary(query):
    """
    Fetch Reddit thread summary for a given query.

    Args:
        query (str): Search term

    Returns:
        str: Summary or placeholder
    """
    try:
        url = f"https://www.reddit.com/search.json?q={query}&limit=5"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json().get("data", {}).get("children", [])

        if not data:
            return "No Reddit threads found."

        top_post = data[0]["data"]
        title = top_post.get("title", "No title")
        score = top_post.get("score", 0)
        comments = top_post.get("num_comments", 0)

        return f"Top thread: \"{title}\" | Score: {score} | Comments: {comments}"

    except Exception as e:
        print(f"[Reddit] Error fetching threads: {e}")
        return "Reddit data unavailable."

def format_alert(signal):
    return f"""
🚨 *New Signal: ${signal['ticker']}*
📈 *Price:* ${signal['price']} | *Change:* {signal['change']}%
🧠 *AI Score:* {signal['score']}/10
📰 *News:* {signal.get('top_news', 'No news found')}
💬 *Reddit:* {signal.get('reddit_summary', 'No Reddit data')}
🐦 *Twitter:* {signal.get('twitter_summary', 'No Twitter data')}
🔗 [View Chart]({signal.get('chart_url', '#')})
"""

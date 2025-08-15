function showTable(type) {
  document.getElementById('crypto-table').style.display = type === 'crypto' ? 'block' : 'none';
  document.getElementById('stocks-table').style.display = type === 'stocks' ? 'block' : 'none';
  document.getElementById('watchlist-table').style.display = type === 'watchlist' ? 'block' : 'none';
}

function addToWatchlist(ticker) {
  fetch(`/watchlist/add/${ticker}`, { method: 'POST' })
    .then(() => alert(`${ticker} added to watchlist`));
}

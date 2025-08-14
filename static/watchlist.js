async function loadWatchlist() {
  const res = await fetch("/api/watchlist");
  const data = await res.json();
  const table = document.getElementById("watchlist-table");
  table.innerHTML = "";

  data.forEach(item => {
    const row = document.createElement("tr");
    row.className = item.sentiment === "bullish" ? "bg-green-100" : item.sentiment === "bearish" ? "bg-red-100" : "";

    row.innerHTML = `
      <td>${item.ticker}</td>
      <td>${item.type}</td>
      <td title="AI Score">${item.ai_score}</td>
      <td title="Sentiment">${item.sentiment}</td>
      <td>${item.catalyst || "—"}</td>
      <td>${new Date(item.last_scan).toLocaleString()}</td>
      <td>
        <button onclick="viewDetails('${item.ticker}')">View</button>
        <button onclick="removeFromWatchlist('${item.ticker}')">Remove</button>
      </td>
    `;
    table.appendChild(row);
  });
}

async function removeFromWatchlist(ticker) {
  await fetch(`/api/watchlist/remove/${ticker}`, { method: "POST" });
  loadWatchlist();
}

function viewDetails(ticker) {
  // Modal logic here
}

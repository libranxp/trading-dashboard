async function runScan() {
  const res = await fetch('/scan');
  const data = await res.json();
  const tbody = document.getElementById('scan-results');
  tbody.innerHTML = '';

  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${row.ticker}</td>
      <td>${row.score}</td>
      <td>${row.sentiment}</td>
      <td>${row.volume}</td>
      <td>${row.catalyst}</td>
      <td>${row.time}</td>
    `;
    tbody.appendChild(tr);
  });
}

function toggleAsset() {
  alert("Asset type toggled (placeholder)");
}

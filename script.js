async function fetchDeals(platform) {
  const res = await fetch(`${API_BASE}/api/deals/${platform}`);
  const data = await res.json();
  const container = document.getElementById("product-list");
  container.innerHTML = data.map(item => `
    <div class='card'>
      <img src='${item.image}' alt='${item.title}' />
      <h3>${item.title}</h3>
      <p>💰 ${item.discount_percentage}% OFF</p>
      <a href='${item.url}' target='_blank'>View Deal</a>
    </div>`).join("");
}
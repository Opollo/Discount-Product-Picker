// script.js

// Container where all deals will appear
const dealsContainer = document.getElementById("deals-container");

// Dummy fallback data
const dummyData = {
  amazon: [
    { name: "Wireless Earbuds", price: "$25", discount: "50%", image: "https://via.placeholder.com/150", link: "#" },
    { name: "Smart Watch", price: "$40", discount: "30%", image: "https://via.placeholder.com/150", link: "#" }
  ],
  alibaba: [
    { name: "LED Desk Lamp", price: "$15", discount: "40%", image: "https://via.placeholder.com/150", link: "#" },
    { name: "Portable Fan", price: "$10", discount: "25%", image: "https://via.placeholder.com/150", link: "#" }
  ],
  jumia: [
    { name: "Smartphone Case", price: "$5", discount: "60%", image: "https://via.placeholder.com/150", link: "#" },
    { name: "Wireless Mouse", price: "$12", discount: "45%", image: "https://via.placeholder.com/150", link: "#" }
  ]
};

// Show a loading message while fetching
function showLoading(show = true) {
  dealsContainer.innerHTML = show ? "<p>Loading deals...</p>" : "";
}

// Display deals for each platform
function displayDeals(data) {
  dealsContainer.innerHTML = ""; // Clear previous content

  for (const platform in data) {
    const platformDeals = data[platform];
    if (!platformDeals || platformDeals.length === 0) continue;

    // Platform section
    const platformSection = document.createElement("div");
    platformSection.classList.add("platform-section");

    const title = document.createElement("h2");
    title.textContent = platform.toUpperCase();
    platformSection.appendChild(title);

    // Deal cards
    platformDeals.forEach(deal => {
      const card = document.createElement("div");
      card.classList.add("deal-card");

      card.innerHTML = `
        <img src="${deal.image || 'https://via.placeholder.com/150'}" alt="${deal.name}" />
        <h3>${deal.name}</h3>
        <p>Price: ${deal.price}</p>
        ${deal.discount ? `<p>Discount: ${deal.discount}</p>` : ""}
        ${deal.link ? `<a href="${deal.link}" target="_blank">View Product</a>` : ""}
      `;

      platformSection.appendChild(card);
    });

    dealsContainer.appendChild(platformSection);
  }
}

// Fetch deals from the backend API with fallback to dummy data
async function fetchDeals() {
  showLoading(true);

  try {
    const response = await fetch("http://localhost:5000/api/deals");
    if (!response.ok) throw new Error("Failed to fetch deals from API.");

    const data = await response.json();
    displayDeals(data);
  } catch (error) {
    console.warn(error.message, "Using fallback dummy data.");
    displayDeals(dummyData);
  }
}

// Initialize
fetchDeals();

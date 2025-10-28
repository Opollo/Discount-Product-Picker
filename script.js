// === Container where all deals will appear ===
const dealsContainer = document.getElementById("deals-container");

// Fallback dummy data
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

// Show loading message
function showLoading(show = true) {
  dealsContainer.innerHTML = show ? "<p>Loading deals...</p>" : "";
}

// Render deals
function displayDeals(data) {
  deals

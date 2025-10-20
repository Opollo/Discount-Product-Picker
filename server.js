// server.js
import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// Example function to simulate fetching deals from different platforms
async function fetchDeals() {
  return {
    amazon: [
      { name: "Wireless Earbuds", price: "$29.99", link: "https://amazon.com" },
      { name: "Smart Watch", price: "$45.99", link: "https://amazon.com" },
    ],
    alibaba: [
      { name: "Bluetooth Speaker", price: "$12.50", link: "https://alibaba.com" },
      { name: "LED Light Bulbs", price: "$9.99", link: "https://alibaba.com" },
    ],
    jumia: [
      { name: "Power Bank", price: "UGX 35,000", link: "https://jumia.ug" },
      { name: "Flash Drive 32GB", price: "UGX 22,000", link: "https://jumia.ug" },
    ],
  };
}

// Endpoint to fetch deals
app.get("/api/deals", async (req, res) => {
  try {
    const deals = await fetchDeals();
    res.json(deals);
  } catch (error) {
    console.error("Error fetching deals:", error);
    res.status(500).json({ error: "Failed to fetch deals" });
  }
});

app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));

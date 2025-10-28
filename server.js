import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// ✅ Dummy data for all platforms
const SAMPLE_DEALS = {
  amazon: [
    { name: "Wireless Earbuds", price: "$29.99", discount: "40%", link: "https://amazon.com" },
    { name: "Smart Watch", price: "$45.99", discount: "25%", link: "https://amazon.com" },
  ],
  alibaba: [
    { name: "Bluetooth Speaker", price: "$12.50", discount: "30%", link: "https://alibaba.com" },
    { name: "LED Light Bulbs", price: "$9.99", discount: "20%", link: "https://alibaba.com" },
  ],
  jumia: [
    { name: "Power Bank", price: "UGX 35,000", discount: "15%", link: "https://jumia.ug" },
    { name: "Flash Drive 32GB", price: "UGX 22,000", discount: "10%", link: "https://jumia.ug" },
  ],
};

// Simulate fetching deals (could be replaced with real API calls)
async function fetchDeals(platform = null) {
  if (!platform) return SAMPLE_DEALS;
  platform = platform.toLowerCase();
  if (!SAMPLE_DEALS[platform]) throw new Error(`Platform '${platform}' not found`);
  return { [platform]: SAMPLE_DEALS[platform] };
}

// Endpoint: Get all d

# Smart Electronic Inventory System

A simple command-line inventory management system for an electronics shop with a built-in AI Assistant.

## Features

- Product, Category, Supplier & Customer management
- Sales recording (automatically updates stock)
- Inventory management & low stock alerts
- Reports (sales & inventory value)
- AI Assistant (fast/slow movers, stockout risk, overstock, restock recommendations)

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Load sample data
python seed_sample_data.py

# 3. Start the application
python main.py
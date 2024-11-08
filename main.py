import requests
import yfinance as yf
import tkinter as tk

# Setting up Alpha Vantage API key and base URL
ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY"  # Replace with your actual Alpha Vantage API key. It's free by signing up
ALPHA_VANTAGE_SEARCH_URL = "https://www.alphavantage.co/query"


def search_company_name(company_name):
    # To fetch the closest matching stock symbol for a company name
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": company_name,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(ALPHA_VANTAGE_SEARCH_URL, params=params)
    data = response.json()
    best_matches = data.get("bestMatches", [])
    if best_matches:
        return best_matches[0]["1. symbol"], best_matches[0]["2. name"]
    else:
        return None, None


def get_stock_price(event=None):
    company_name = company_name_entry.get().strip()
    symbol, actual_name = search_company_name(company_name)
    if not symbol:
        result_label.config(text="No matches found. Please try a different company name.")
        return

    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            price = stock_info['Close'][0]
            result_label.config(text=f"Stock name: {actual_name} ({symbol})\nCurrent price: ${price:.2f}")
        else:
            result_label.config(text=f"No price data available for {actual_name} ({symbol})")

    except Exception as e:
        result_label.config(text=f"Error retrieving data for {actual_name} ({symbol})")


# Setup tkinter window
root = tk.Tk()
root.title("Stock Price Checker")

# Input label and text entry box
company_name_label = tk.Label(root, text="Enter Company Name:")
company_name_label.pack()

company_name_entry = tk.Entry(root)
company_name_entry.pack()

# Bind Enter key to the get_stock_price function
company_name_entry.bind("<Return>", get_stock_price)

# Search button
search_button = tk.Button(root, text="Get Price", command=get_stock_price)
search_button.pack()

# Label to display results
result_label = tk.Label(root, text="")
result_label.pack()

# Run the Tkinter loop
root.mainloop()

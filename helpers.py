import csv
import datetime
import pytz
import requests
import time

from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """Escape special characters."""
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    """Look up quote for symbol."""
    
    # Prepare API request
    symbol = symbol.upper()

    # Yahoo Finance API URL
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{symbol}.NS"
        f"?region=US&lang=en-US&includePrePost=false"
        f"&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
    }
    session = requests.Session()

    for attempt in range(5):  # Retry up to 5 times
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            result = data.get("chart", {}).get("result", [])
            if not result:
                print("No results found.")
                return None

            # Extracting the latest quote data
            quote = result[0]
            price = round(float(quote["meta"]["regularMarketPrice"]), 2)
            name = quote["meta"]["longName"]
            return {
                "name": name,
                "price": price,
                "symbol": symbol
            }
        except requests.RequestException as e:
            if response.status_code == 429:
                print(f"Rate limit exceeded. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Error: {e}")
                return None
        except (ValueError, KeyError, IndexError) as e:
            print(f"Error processing data: {e}")
            return None

    print("Failed to retrieve data after several attempts.")
    return None

def inr(value):
    """Format value as INR."""
    return f"₹{value:,.2f}"

# FinBha₹at

FinBha₹at is a web application designed to help users manage a virtual stock portfolio, specifically tailored for the Indian stock market. It is an alternative to CS50's Finance course project, customized with additional features and functionality.

## Features

- **User Authentication:**
  - **Secure User Login and Registration:** Users can securely register and log in using hashed passwords. Session management maintains user-specific data throughout their session.
  
- **Stock Management:**
  - **Buy Stocks:** Users can purchase shares of stocks with real-time price updates from the Indian stock market (NSE). The portfolio and cash balance are updated automatically.
  - **Sell Stocks:** Users can sell stocks from their portfolio. The portfolio and cash balance are updated in real-time after a sale.

- **Portfolio Tracking:**
  - **View Portfolio:** Displays current stock holdings, including stock symbols, quantities, and market values. Users can see a detailed view of their investments.
  - **Transaction History:** Provides a comprehensive history of all stock transactions, including purchases and sales, helping users track their trading activities.

- **Stock Lookup:**
  - **Get Stock Quotes:** Retrieve real-time stock quotes and company information from external data services to make informed trading decisions.

- **Cash Management:**
  - **Current Cash Balance:** Shows the available cash balance for transactions and updates it automatically after trades.

- **User Interface:**
  - **Responsive Web Interface:** A clean and intuitive web interface built with HTML5, CSS, and Bootstrap for a responsive and user-friendly experience. Dynamic templates are used for portfolio management, transaction history, and stock management.

- **Database Integration:**
  - **SQLite:** Utilizes a local SQLite database for managing user data, transactions, and stock information. Ensures reliable data storage and retrieval.

- **Security:**
  - **Secure Password Handling:** User passwords are securely hashed and managed. Session management ensures that user data is protected throughout the session.

- **Error Handling:**
  - **Informative Error Messages:** Includes validation checks and informative error messages to provide a smooth user experience and guide users through any issues.

## Technologies Used

- **Frontend:**
  - HTML
  - CSS
  - Bootstrap 5
  - Font Awesome

- **Backend:**
  - Python
  - Flask

- **APIs:**
  - Yahoo Finance for stock data

- **Database:**
  - SQLite

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/thesupersaurabh/FinBharat.git
    cd finbharat
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate` or in vscode terminal `.\venv\Scripts\Activate.ps1`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    flask run
    ```

    The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- **Register:** Create a new account to start managing your portfolio.
- **Log In:** Access your portfolio and manage your stocks.
- **Buy Stocks:** Enter the stock symbol and number of shares to purchase.
- **Sell Stocks:** Select a stock from your portfolio and specify the number of shares to sell.
- **View History:** Check your transaction history for a detailed overview.
- **Get Quotes:** Enter a stock symbol to retrieve its current price.

## Contributing

Contributions are welcome! Please submit a pull request with a description of your changes or improvements.

## Acknowledgments

- **Bootstrap:** For the beautiful UI components.
- **Font Awesome:** For the icons.
- **Yahoo Finance API:** For stock data.

## Contact

For any inquiries or feedback, please reach out to [Saurabh](https://thesaurabh.me).

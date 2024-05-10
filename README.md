# Binance Price Tracker

BinancePriceTracker is a real-time connection to the Binance WebSocket to capture and process the prices of given
cryptocurrencies (Currently added 21 cryptocurrencies). It stores the captured price data and offers API endpoints for
users to access current prices, historical data, and perform basic statistical analysis on these data.

## Features

- Establish a connection to the Binance WebSocket and subscribes to the 'trade' WebSocket streams for selected
  cryptocurrency pairs.
- Extract price information from each trade message received and stores it in a database.
- Implement efficient management of the WebSocket connection and incoming data stream, considering Binance API rate
  limits.
- Offer three RESTful API endpoints for:
    - Retrieving the latest price of a given cryptocurrency.
    - Retrieving historical price data within a user given date range.
    - Performing statistical analysis on stored data (Addition: user can perform statistical analysis within a given
      date range).
- Provide thorough documentation and a comprehensive suite of unit tests.

## Requirements

- Python 3.7 or higher
- See `requirements.txt` for Python package dependencies.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KamranKhalid044/BinancePriceTracker.git
   cd BinancePriceTracker

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

## Scripts Overview

- **models.py**: Define the database schema using SQLAlchemy ORM and create necessary indexes.
- **data_manager.py**: Contain function for saving trade data to the database.
- **websocket_trade_handler.py**: Implement the WebSocket connection to Binance, subscribe to trade streams, and handle
  incoming trade data.
- **app.py**: Implement Flask API endpoints for trade data retrieval and analysis.
- **test_api_endpoints.py**: Contain unit tests for the API endpoints defined in `app.py`.

## Running websocket_trade_handler to Get Data

To start capturing and processing cryptocurrency prices:

1. Ensure that all dependencies are installed.
2. Run the WebSocket trade handler script:
   ```bash
   python websocket_trade_handler.py

## Running the Flask API

To run the Flask APIs for the Binance Price Tracker, follow these steps (**Skip below step(s) if already done as mentioned above**):
1. **Ensure Python and Dependencies are Installed**:
   - Make sure you have Python 3.7 or higher installed on your system.
   - Install the required Python packages listed in the `requirements.txt` file. You can do this using pip:

   ```bash
   pip install -r requirements.txt

2. **Start the Flask Application**:
   - Navigate to the directory where the `app.py` file is located.
   - Run the Flask application by executing the following command in your terminal:

   ```bash
   python app.py

3. **Accessing the API Endpoints**:
   - Once the Flask application is running, you can access the API endpoints using tools like cURL, Postman, or by making HTTP requests from your web browser or other applications.
   - See `README (API Documentation).md` for API endpoints and their functionalities

4. **Stopping the Flask Application**:
   - To stop the Flask application, press `Ctrl + C` in the terminal window where the application is running. This will shut down the Flask server.
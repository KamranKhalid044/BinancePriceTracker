# Binance Price Tracker

BinancePriceTracker is a real-time connection to the Binance WebSocket to capture and process the prices of given
cryptocurrencies (Currently added 21 cryptocurrencies). It stores the captured price data and offers API endpoints for
users to access current prices, historical data, and perform basic statistical analysis on these data.

## Features

- Establishe a connection to the Binance WebSocket and subscribes to the 'trade' WebSocket streams for selected
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

## How to Run

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
   - The API endpoints and their functionalities are documented **below after point 4**

4. **Stopping the Flask Application**:
   - To stop the Flask application, press `Ctrl + C` in the terminal window where the application is running. This will shut down the Flask server.

##Current Price Endpoint
### Retrieving the latest Current Price of a Specific Cryptocurrency
 - Endpoint URL: `http://localhost:5000/current_price`
 - Method: `GET`
 - Parameters: 
   - `symbol`: The symbol of the cryptocurrency for which you want to retrieve the current price.
 
### Request
GET http://localhost:5000/current_price?symbol=DOTUSDT

### Response
- **Status Code**: 200 OK
    ```json
    {
      "price": 6.952,
      "symbol": "DOTUSDT"
    }

### Requests
GET http://localhost:5000/current_price

GET http://localhost:5000/current_price?symbol=

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Please provide a valid symbol parameter"
    }
  
### Request
GET http://localhost:5000/current_price?symbol=DOTUSDT,DOTUSDT

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Only one symbol parameter is allowed"
    }
  
### Request
GET http://localhost:5000/current_price?symbol=DOTUSD

### Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Symbol does not exist in the database"
    }

### Request
GET http://localhost:5000/current_price?symbol=DOTBCT

### Sample Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Data not found for the specified symbol"
    }
  
### Request
GET http://localhost:5000/current_price?symbol=XYZ

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Database error: <error_details>"
    }

### Request
GET http://localhost:5000/current_price?symbol=XYZ

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Error occurred while fetching current price: <error_details>"
    }

##Historical Data Endpoint
### Retrieving Historical Price Data for a User-Specified Date Range

Retrieving historical price data within a user-specified date range, users can specify their desired timeframe using start and end date parameters in their requests. The date format for these parameters are "YYYY-MM-DD HH:MM:SS".

For example:
- `start_date`: "2023-01-01 00:00:00"
- `end_date`: "2023-12-31 23:59:59"

Users can then make requests to retrieve historical price data within this specified date range.

 - Endpoint URL: `http://localhost:5000/historical_data`
 - Method: `GET`
 - Parameters: 
   - `symbol`: The symbol of the cryptocurrency for which you want to retrieve historical data.
   - `start_date`: The start date of the historical data range in the format `YYYY-MM-DD HH:MM:SS`.
   - `end_date`: The end date of the historical data range in the format `YYYY-MM-DD HH:MM:SS`.
   - Optional Parameters: 
     - `page`: The page number for paginated results (default is 1).
     - `per_page`: The number of items per page (default is 10).

### Request
GET http://localhost:5000/historical_data?symbol=VETUSDT&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:12

### Response
- **Status Code**: 200 OK
    ```json
    {
        "data": [
            {
                "price": 0.03493,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 13:10:12"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:54"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:54"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:54"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:53"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:52"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:52"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:52"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:52"
            },
            {
                "price": 0.03499,
                "symbol": "VETUSDT",
                "timestamp": "2024-05-08 12:57:52"
            }
        ],
        "total_items": 11,
        "total_pages": 2
    }
  
### Requests
GET http://localhost:5000/historical_data

GET http://localhost:5000/historical_data?symbol=VETUSDT

GET http://localhost:5000/historical_data?symbol=VETUSDT&start_date=2024-05-08%2012:57:51

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Please provide symbol, start_date, and end_date parameters"
    }
  
### Request
GET http://localhost:5000/historical_data?symbol=VETUSDT&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Invalid date format, date format must be YYYY-MM-DD HH:MM:SS"
    }
  
### Request
GET http://localhost:5000/historical_data?symbol=VETUSDT&start_date=2024-09-08%2012:57:51&end_date=2024-05-08%2013:10:12

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Start date must be earlier than the end date"
    }
  
### Request
GET http://localhost:5000/historical_data?symbol=VETUSD&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:12

### Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Symbol does not exist in the database"
    }

### Request
GET http://localhost:5000/historical_data?symbol=SOLUSDT&start_date=2024-05-10 04:09:40&end_date=2024-05-10 04:09:41

### Sample Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Data not found for the specified date range"
    }
  
### Request
GET http://localhost:5000/historical_data?symbol=VETUSDT&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:12&page=2&per_page=10

### Sample Response
- **Status Code**: 404 Not Found
    ```json
    {
        "message": "Requested page is out of range. Please provide a valid page number",
        "total_items": 10,
        "total_pages": 1
    }
  
### Request
GET http://localhost:5000/historical_data?symbol=XYZ&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:12&page=1&per_page=2

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Database error: <error_details>"
    }

### Request
GET http://localhost:5000/historical_data?symbol=XYZ&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:12&page=1&per_page=2

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Error occurred while fetching historical data: <error_details>"
    }
  
##Statistical Analysis Endpoint
###Perform Basic Statistical Analyses for Cryptocurrency Data
1. **Average Price:** The average price of the specified cryptocurrency is calculated by summing up all the prices and dividing by the total number of data points.
2. **Median Price:** The median price represents the middle value of the dataset when arranged in ascending order. It divides the dataset into two equal halves.
3. **Standard Deviation:** The standard deviation measures the dispersion or variability of prices from the average price. It indicates how much the prices deviate from the mean.
4. **Percentage Change:** The percentage change compares the current price of the cryptocurrency with its previous price and expresses it as a percentage.

 - Endpoint URL: `http://localhost:5000/statistical_analysis`
 - Method: `GET`
 - Parameters: 
   - `symbol`: The symbol of the cryptocurrency for which you want to perform statistical analysis.
   - Optional Parameters:
     - `start_date`: The start date of the data range for analysis in the format `YYYY-MM-DD HH:MM:SS` (default is None).
     - `end_date`: The end date of the data range for analysis in the format `YYYY-MM-DD HH:MM:SS` (default is None).

### Request
GET http://localhost:5000/statistical_analysis?symbol=VETUSDT

### Response
- **Status Code**: 200 OK
    ```json
    {
        "average_price": 0.03,
        "median_price": 0.03499,
        "percentage_change": 0.17,
        "standard_deviation": 0.0,
        "symbol": "VETUSDT"
    }
  
### Requests
GET http://localhost:5000/statistical_analysis

GET http://localhost:5000/statistical_analysis?symbol=

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Please provide a valid symbol parameter"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=DOTUSDT,DOTUSDT

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Only one symbol parameter is allowed"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=VETUSDT&start_date=2024-05-08%2012:57:51&end_date=2024-05-08%2013:10:

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Invalid date format, date format must be YYYY-MM-DD HH:MM:SS"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=VETUSDT&start_date=2024-09-08%2012:57:51&end_date=2024-05-08%2013:10:12

### Response
- **Status Code**: 400 Bad Request
    ```json
    {
        "error": "Start date must be earlier than the end date"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=VETUSD

### Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Symbol does not exist in the database"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=SOLUSDT&start_date=2024-05-10 04:09:40&end_date=2024-05-10 04:09:41

### Sample Response
- **Status Code**: 404 Not Found
    ```json
    {
        "error": "Data not found for the specified date range"
    }
  
### Request
GET http://localhost:5000/statistical_analysis?symbol=XYZ

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Database error: <error_details>"
    }

### Request
GET http://localhost:5000/statistical_analysis?symbol=XYZ

### Sample Response
- **Status Code**: 500 Internal Server
    ```json
    {
        "error": "Error occurred while performing statistical analysis: <error_details>"
    }

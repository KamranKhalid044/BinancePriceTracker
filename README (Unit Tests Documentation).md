# Unit Tests Documentation

## Overview

This module contains unit tests for the API endpoints of the application.

These tests validate the behavior of the API endpoints including:
- Successful retrieval of current price
- Handling of various error cases such as missing symbols or database errors
- Retrieval of historical data within a specified date range
- Statistical analysis of trade data including average price, median price,
  standard deviation, and percentage change over time

## Running the Tests

To run these unit tests, follow these steps:

1. **Setup Environment:** Ensure that you have the necessary dependencies installed. Typically, this involves having Python installed, which includes the `unittest` library.

2. **Clone the Repository:** Clone the repository containing the application code and navigate to the directory containing the tests.

3. **Run the Tests:** Execute the test runner script or command in the terminal:
   ```bash
   python test_api_endpoints.py

This command will run all the test cases defined in the specified test script. You should see the test results displayed in the terminal.

4. **Interpreting Results:** After running the tests, review the output to ensure that all tests pass. Any failures or errors should be investigated and addressed.

By following these steps, you can verify the functionality and correctness of the API endpoints through automated unit tests using the `unittest` library.
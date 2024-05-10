# Database Design Documentation

**1. Introduction:**
The database is designed to store cryptocurrency trade data from the Binance exchange. It's structured to efficiently store and retrieve trade information such as the symbol (cryptocurrency symbol), price, and timestamp of each trade.

**2. Entity-Relationship Diagram (ERD):**

|   Table: trades     |
|-------------------|

| Field     | Type    |
|-----------|---------|
| id (PK)   | Integer |
| symbol    | String  |
| price     | Float   |
| timestamp | DateTime|


**3. Table Description:**

**trades:**
- This table stores the trade data.
- Each row represents a single trade.
- Attributes:
  - id: Primary Key, unique identifier for each trade.
  - symbol: Symbol of the cryptocurrency being traded.
  - price: Price of the cryptocurrency at the time of the trade.
  - timestamp: Timestamp of when the trade occurred.

**4. Indexing:**
An index named `trade_symbol_index` is created on the `symbol` column of the `trades` table to optimize search queries based on the cryptocurrency symbol.

**5. Design Choices and Justifications:**
- **SQLite Database:** SQLite is chosen for its simplicity, portability, and compatibility with SQLAlchemy. It's suitable for small to medium-sized applications like this.
- **Single Table:** Given the relatively simple structure of the data, a single table design is chosen to avoid unnecessary complexity.
- **Column Types:** 
  - Integer for the primary key (`id`).
  - String for `symbol`, as it can contain alphanumeric characters.
  - Float for `price`, to accurately represent decimal numbers.
  - DateTime for `timestamp`, to store the precise time of each trade.
- **Default Timestamp:** The `timestamp` column has a default value to automatically insert the current timestamp when a new trade is added.
- **Indexing:** An index is added to the `symbol` column to improve the performance of queries filtering by symbol.

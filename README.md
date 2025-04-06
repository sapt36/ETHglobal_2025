# 1inch Dev Backend Service

This project uses Flask as the backend framework and integrates the [1inch Dev API](https://docs.1inch.io/api) to provide a variety of blockchain-related query functions, including **Token Balances, Token Prices, NFT Information, OrderBook, Gas Price,** and more. It also leverages a simple **in-memory Cache** to optimize request speeds.

---

## Table of Contents
1. [Feature Overview](#feature-overview)
2. [Environment Requirements](#environment-requirements)
3. [Installation and Execution](#installation-and-execution)
4. [API Documentation](#api-documentation)
    - [1. CombinedBalance](#1-combinedbalance)
    - [2. TokenBalance / TokenInfo](#2-tokenbalance--tokeninfo)
    - [3. Chart (Token / NaiveChain / HistoryTokenPrice)](#3-chart-token--naivechain--historytokenprice)
    - [4. OrderBook (ByHash / ByWallet)](#4-orderbook-byhash--bywallet)
    - [5. NFT (by address)](#5-nft-by-address)
    - [6. GasPrice](#6-gasprice)
    - [7. Sample Data](#7-sample-data)
5. [Cache Mechanism](#cache-mechanism)
6. [Additional Notes](#additional-notes)
7. [License](#license)

---

## Feature Overview

- **Multi-Chain Support**: Supports Ethereum, BSC, Polygon, Avalanche, Arbitrum, Optimism, etc. (You can customize within `CHAIN_IDS`)  
- **Token / NFT Queries**: Retrieve wallet balances, detailed Token information (name, logo), and NFT information (name, image URL)  
- **Historical Prices/Charts**: Utilize 1inch-provided Token charts, historical price ranges, Gas prices, and other APIs  
- **In-Memory Cache**: Reduce duplicate calls to external services, lowering wait times and API traffic

---

## Environment Requirements

1. **Python 3.7+**  
2. [pip](https://pip.pypa.io/en/stable/) installed  
3. Installed packages: [Flask](https://pypi.org/project/Flask/), [Requests](https://pypi.org/project/requests/), [python-dotenv](https://pypi.org/project/python-dotenv/), [Flask-Cors](https://pypi.org/project/Flask-Cors/)  
4. An **API Key** from [1inch Dev](https://docs.1inch.io/api) (to be placed in the `.env` file)

---

## Installation and Execution

1. **Download/Clone the Project**

   ```bash
   git clone https://github.com/your-repo/1inch-backend.git
   cd 1inch-backend
   ```
2. **Install Packages**  
   If you do not have a `requirements.txt`, install manually:
   ```bash
   pip install flask requests python-dotenv flask-cors
   ```
3. **Configure `.env`**  
   Create a `.env` file in the project root with the following content:
   ```bash
   1INCH_API_KEY=YOUR_1INCH_KEY
   WALLET_ADDRESS=YOUR_DEFAULT_WALLET_ADDRESS
   ```
   > `WALLET_ADDRESS` is optional and is only used as an example in the code.

4. **Run the Backend**  
   ```bash
   python app.py
   ```
   The service will run on `http://127.0.0.1:5000` by default.  
   (If the file is not named `app.py`, please replace it with your filename.)

---

## API Documentation

### 1. CombinedBalance
- **Endpoint**: `/api/Token/CombinedBalance/<network>/<wallet_address>`
- **Method**: `GET`
- **Functionality**: 
  - First, query the Token balances for the specified `wallet_address` on the given `network` using `balance/v1.2`  
  - Then, for each Token, call `token/v1.2/custom/{tokenAddress}` to retrieve **Token Name, Decimals, Logo URI**  
  - Utilizes an in-memory Cache to avoid repeated queries in a short time period
- **Example**:  
  ```
  GET /api/Token/CombinedBalance/ethereum/0xYourWallet
  ```

### 2. TokenBalance / TokenInfo
- **`/api/Token/TokenBalance/<network>/<wallet_address>`**  
  - Retrieves the Token balances for the wallet on the specified network (excluding additional Token details)
- **`/api/Token/TokenInfo/<network>/<token_address>`**  
  - Retrieves detailed information for the specified Token contract, including name, symbol, logoURI, etc.

### 3. Chart (Token / NaiveChain / HistoryTokenPrice)
- **`/api/Chart/Token/<network>/<token_address>`**  
  - Calls the `token-details/v1.0/charts` endpoint with parameters such as interval and from_time
- **`/api/Chart/NaiveChain/<network>`**  
  - Similar to the above, but only passes the chainId without a token_address
- **`/api/Chart/HistoryTokenPrice/<network>/<TimeFrom>/<TimeTo>/<token_address>`**  
  - Retrieves historical price data within a custom interval (`from` / `to`)

### 4. OrderBook (ByHash / ByWallet)
- **`/api/OrderBook/Hash/<network>/<hash_address>`**  
  - Retrieves OrderBook information using a transaction hash  
- **`/api/OrderBook/Wallet/<network>/<wallet_address>`**  
  - Retrieves OrderBook information based on a wallet address

### 5. NFT (by address)
- **`/api/NFT/<wallet_address>`**  
  - Calls the `nft/v2/byaddress` endpoint, supporting multiple chains  
  - Returns a JSON structure in the format: `{ "NFT Name": "NFT Image URL", ... }`

### 6. GasPrice
- **`/api/GasPrice/<network>`**  
  - Retrieves the current Gas Price information for the specified network

### 7. Sample Data
- **`/api/data`**  
  - A simple test endpoint that returns example JSON: `{"id":1,"name":"Alice","message":"Hello from Python backend"}`

---

## Cache Mechanism

- An in-memory global dictionary named `combined_balance_cache` is used to cache results for certain API calls (such as `get_CombinedBalance`).  
- **TTL** (Time-To-Live) is set to `CACHE_TTL_SECONDS = 12000` seconds (approximately 3.3 hours) by default, but can be adjusted as needed.  
- If a valid cache entry is found within the TTL, the cached data is returned; otherwise, a call to the 1inch API is made.

> **Note**: This in-memory cache works under a **single backend instance**. For multiple backend instances or a more robust caching solution, consider using an external service like Redis.

---

## Additional Notes

1. **CORS**  
   - Using `Flask-Cors` and applying `CORS(app)` or `@cross_origin()` in the code allows cross-domain requests from the frontend.
2. **Throttling / Rate Limit**  
   - Some parts of the code use `time.sleep(0.5)` to reduce the rate of simultaneous requests to the 1inch API.  
   - For more comprehensive rate limiting, consider integrating [Flask-Limiter](https://pypi.org/project/Flask-Limiter/).
3. **API Key Protection**  
   - Ensure the `1INCH_API_KEY` is stored in the `.env` file and **do not** upload this key to public repositories.
4. **Network Mapping**  
   - The `CHAIN_IDS` variable defines the chainIds (as numbers) for common networks; expand or modify as needed.

---

## License

This project is released under the MIT License. Please refer to the [LICENSE](LICENSE) file for details (or add one if it is not present).

If you have any questions or suggestions, feel free to open an Issue or submit a Pull Request. Thank you for using this project!

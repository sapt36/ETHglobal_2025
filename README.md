# 1inch Dev Backend Service

<p align="center">
<img src="https://github.com/user-attachments/assets/7ef14ede-b98a-4ba6-9c87-a734265ca422">
</p>

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

### API Documentation

This document describes the RESTful APIs provided by the backend Flask application, which integrates with the 1inch.dev API to retrieve various blockchain-related data.

### Base URL

`http://127.0.0.1:5000` (or your deployed server address)

### Authentication

All API calls to 1inch.dev require an `Authorization` header with a Bearer token. This token (`my_1inch_api_key`) should be configured as an environment variable on the server.

### Network Chain IDs

The following table lists the supported network names and their corresponding Chain IDs used throughout the APIs:

| Network Name | Chain ID (Decimal) |
| --- | --- |
| `rabbithole` | `1` |
| `aurora` | `1313161554` |
| `arbitrum` | `42161` |
| `avalanche` | `43114` |
| `base` | `8453` |
| `linea` | `59144` |
| `binance` | `56` |
| `fantom` | `250` |
| `gnosis` | `100` |
| `kaia` | `8217` |
| `optimistic` | `10` |
| `polygon` | `137` |
| `zksync` | `324` |
| `ethereum` | `1` |

### Endpoints

### 1. Get Example Data

- **Endpoint:** `/api/data`
- **Method:** `GET`
- **Description:** Returns simple example data from the backend.
- **Response:**
    - `200 OK`
    
    ```
    {
      "id": 1,
      "name": "Alice",
      "message": "Hello from Python backend"
    }
    
    ```
    

### 2. Get Chart Data for a Specific Token

- **Endpoint:** `/api/Chart/Token/<network>/<token_address>`
- **Method:** `GET`
- **Description:** Retrieves historical price chart data for a specific token on a given network.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name (e.g., `ethereum`, `polygon`).
    - `token_address` (string, required): The contract address of the token.
- **Query Parameters (Internal to 1inch API):**
    - `interval` (string): Time interval for chart data. Default `24h, 1w, 1m, 1y`.
    - `from_time` (string): Start timestamp for data in Unix epoch seconds. Default `1631644261`.
- **Response:**
    - `200 OK`: JSON object containing chart data as returned by the 1inch.dev API.
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 3. Get Chart Data for a Native Chain

- **Endpoint:** `/api/Chart/NaiveChain/<network>`
- **Method:** `GET`
- **Description:** Retrieves historical price chart data for the native token of a given blockchain network.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name (e.g., `ethereum`, `polygon`).
- **Query Parameters (Internal to 1inch API):**
    - `interval` (string): Time interval for chart data. Default `24h, 7d, 30d, 365d`.
    - `from_time` (string): Start timestamp for data in Unix epoch seconds. Default `1631644261`.
- **Response:**
    - `200 OK`: JSON object containing chart data as returned by the 1inch.dev API.
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 4. Get Historical Token Price for a Range

- **Endpoint:** `/api/Chart/HistoryTokenPrice/<network>/<TimeFrom>/<TimeTo>/<token_address>`
- **Method:** `GET`
- **Description:** Retrieves historical price data for a specific token within a specified time range.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `TimeFrom` (string, required): Start timestamp in Unix epoch seconds (e.g., `1743844261`).
    - `TimeTo` (string, required): End timestamp in Unix epoch seconds (e.g., `1743854275`).
    - `token_address` (string, required): The contract address of the token.
- **Response:**
    - `200 OK`: JSON object containing historical price data as returned by the 1inch.dev API.
    - `400 Bad Request`: If the `network` is invalid or timestamps are malformed.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 5. Get Order Book by Hash

- **Endpoint:** `/api/OrderBook/Hash/<network>/<hash_address>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific order from the order book using its hash address.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `hash_address` (string, required): The hash address of the order.
- **Response:**
    - `200 OK`: JSON object containing order details as returned by the 1inch.dev API.
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 6. Get Order Book by Wallet Address

- **Endpoint:** `/api/OrderBook/Wallet/<network>/<wallet_address>`
- **Method:** `GET`
- **Description:** Retrieves a list of orders associated with a specific wallet address from the order book.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `wallet_address` (string, required): The wallet address.
- **Query Parameters (Internal to 1inch API):**
    - `limit` (string): Maximum number of orders to return. Default `5`.
- **Response:**
    - `200 OK`: JSON array of order objects as returned by the 1inch.dev API.
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 7. Get Token Balance for a Wallet

- **Endpoint:** `/api/Token/TokenBalance/<network>/<wallet_address>`
- **Method:** `GET`
- **Description:** Retrieves the raw token balances (in smallest units) for all tokens held by a specific wallet on a given network.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `wallet_address` (string, required): The wallet address.
- **Response:**
    - `200 OK`: JSON object where keys are token addresses and values are raw balances.
    
    ```
    {
      "0x...token1_address": "10000000000000000000",
      "0x...token2_address": "500000000000000000"
      // ... more tokens
    }
    
    ```
    
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 8. Get Token Information

- **Endpoint:** `/api/Token/TokenInfo/<network>/<token_address>`
- **Method:** `GET`
- **Description:** Retrieves detailed information (name, decimals, symbol, etc.) about a specific token.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `token_address` (string, required): The contract address of the token.
- **Response:**
    - `200 OK`: JSON object containing token details.
    
    ```
    {
      "symbol": "USDT",
      "name": "Tether USD",
      "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
      "decimals": 6,
      "logoURI": "https://tokens.1inch.io/0xdac17f958d2ee523a2206206994597c13d831ec7.png"
    }
    
    ```
    
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 9. Get Combined Token Balance and Value

- **Endpoint:** `/api/Token/CombinedBalance/<network>/<wallet_address>`
- **Method:** `GET`
- **Description:** Retrieves all token balances for a wallet, converts them to human-readable amounts, and attempts to fetch their USD prices to calculate a combined value. This endpoint includes an in-memory cache with a TTL of `12000` seconds (3 hours 20 minutes) to reduce repeated API calls.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name.
    - `wallet_address` (string, required): The wallet address.
- **Response:**
    - `200 OK`: JSON object where keys are token names and values are their human-readable balances.
    
    ```
    {
      "Wrapped Ether": "0.12345",
      "USD Coin": "1500.75",
      "Uniswap": "5.67",
      "Unknown": "0.0001" // For tokens where name couldn't be retrieved
    }
    
    ```
    
    - `400 Bad Request`: If the `network` is invalid.
    - `500 Internal Server Error`: If there's an issue fetching balances, prices, or token info.

### 10. Get NFTs by Wallet Address

- **Endpoint:** `/api/NFT/<wallet_address>`
- **Method:** `GET`
- **Description:** Retrieves a list of NFTs owned by a specific wallet address across multiple predefined chains.
- **Path Parameters:**
    - `wallet_address` (string, required): The wallet address.
- **Query Parameters (Internal to 1inch API):**
    - `chainIds` (list of integers): The list of chain IDs to query for NFTs. Currently hardcoded to `[1, 137, 8453, 42161, 8217, 43114, 10]`.
- **Response:**
    - `200 OK`: JSON object where keys are NFT names and values are their image URLs.
    
    ```
    {
      "CryptoPunk #1234": "https://example.com/cryptopunk1234.png",
      "Bored Ape Yacht Club #5678": "https://example.com/boredape5678.jpg",
      "My Custom NFT": "No Image" // If image_url is missing
    }
    
    ```
    
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

### 11. Get Gas Price

- **Endpoint:** `/api/GasPrice/<network>`
- **Method:** `GET`
- **Description:** Retrieves current gas price information for a given blockchain network.
- **Path Parameters:**
    - `network` (string, required): The blockchain network name (e.g., `ethereum`, `polygon`).
- **Response:**
    - `200 OK`: JSON object containing gas price details (e.g., `fast`, `standard`, `slow` gas prices in Gwei).
    
    ```
    {
      "fast": "20",
      "standard": "15",
      "slow": "10"
    }
    
    ```
    
    - `400 Bad Request`: If the `network` is invalid.
    - `5xx Server Error`: If there's an issue with the upstream 1inch.dev API or internal server error.

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

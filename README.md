# 1inch Dev Backend Service

本專案使用 Flask 作為後端框架，並整合 [1inch Dev API](https://docs.1inch.io/api) 提供多種區塊鏈相關資訊查詢功能，包括 **Token 餘額、Token 價格、NFT 資訊、OrderBook、Gas Price 等**。同時利用簡易的 **in-memory Cache** 優化部分請求速度。

---

## 目錄
1. [功能簡介](#功能簡介)
2. [環境需求](#環境需求)
3. [安裝與執行](#安裝與執行)
4. [API 介面說明](#api-介面說明)
    - [1. CombinedBalance](#1-combinedbalance)
    - [2. TokenBalance / TokenInfo](#2-tokenbalance--tokeninfo)
    - [3. Chart (Token / NaiveChain / HistoryTokenPrice)](#3-chart-token--naivechain--historytokenprice)
    - [4. OrderBook (ByHash / ByWallet)](#4-orderbook-byhash--bywallet)
    - [5. NFT (by address)](#5-nft-by-address)
    - [6. GasPrice](#6-gasprice)
    - [7. Data 範例](#7-data-範例)
5. [快取機制](#快取機制)
6. [其他注意事項](#其他注意事項)
7. [License](#license)

---

## 功能簡介

- **支援多條鏈**：Ethereum, BSC, Polygon, Avalanche, Arbitrum, Optimism 等 (可於 `CHAIN_IDS` 中自訂)  
- **Token / NFT 查詢**：能查錢包餘額、Token 詳細資訊 (名稱、Logo)、NFT 資訊 (名稱、圖片 URL)  
- **歷史價格/圖表**：可使用 1inch 提供的 Token charts、歷史區間價格、Gas 價格等 API  
- **使用記憶體快取**：減少重複呼叫外部服務，降低等待時間與 API 流量

---

## 環境需求

1. **Python 3.7+**  
2. 已安裝 [pip](https://pip.pypa.io/en/stable/)  
3. 已安裝 [Flask](https://pypi.org/project/Flask/)、[Requests](https://pypi.org/project/requests/)、[python-dotenv](https://pypi.org/project/python-dotenv/)、[Flask-Cors](https://pypi.org/project/Flask-Cors/) 等套件  
4. 需要到 [1inch Dev](https://docs.1inch.io/api) 申請 **API Key** (放在 `.env` 檔內)

---

## 安裝與執行

1. **下載/克隆本專案**  

   ```bash
   git clone https://github.com/your-repo/1inch-backend.git
   cd 1inch-backend
   ```
2. **安裝套件**  
   若沒有 `requirements.txt`，請手動安裝：
   ```bash
   pip install flask requests python-dotenv flask-cors
   ```
3. **設定 `.env`**  
   在專案根目錄新增 `.env` 檔，內容包含：
   ```bash
   1INCH_API_KEY=YOUR_1INCH_KEY
   WALLET_ADDRESS=YOUR_DEFAULT_WALLET_ADDRESS
   ```
   > `WALLET_ADDRESS` 為非必需，只是程式中示例提到可能用到。

4. **執行後端**  
   ```bash
   python app.py
   ```
   預設會在 `http://127.0.0.1:5000` 上運行。  
   （若檔案不叫 `app.py`，請替換為你的檔名。）

---

## API 介面說明

### 1. CombinedBalance
- **路由**: `/api/Token/CombinedBalance/<network>/<wallet_address>`
- **方法**: `GET`
- **功能**: 
  - 先透過 `balance/v1.2` 查詢該 `wallet_address` 在指定 `network` 的所有 Token 餘額  
  - 再逐一呼叫 `token/v1.2/custom/{tokenAddress}` 取得 Token 的 **名稱、Decimals、Logo URI**  
  - 以 in-memory Cache 避免短時間內多次重複查詢
- **範例**:  
  ```
  GET /api/Token/CombinedBalance/ethereum/0xYourWallet
  ```

### 2. TokenBalance / TokenInfo
- **`/api/Token/TokenBalance/<network>/<wallet_address>`**  
  - 取得該 wallet 在 network 上的 Token 餘額 (不包含 Token 其他資訊)
- **`/api/Token/TokenInfo/<network>/<token_address>`**  
  - 取得指定合約 Token 的名稱、符號、logoURI 等詳細資訊

### 3. Chart (Token / NaiveChain / HistoryTokenPrice)
- **`/api/Chart/Token/<network>/<token_address>`**  
  - 呼叫 `token-details/v1.0/charts` 端點，帶入 interval 與 from_time 等參數  
- **`/api/Chart/NaiveChain/<network>`**  
  - 類似上方，但只帶 chainId，不帶 token_address  
- **`/api/Chart/HistoryTokenPrice/<network>/<TimeFrom>/<TimeTo>/<token_address>`**  
  - 自訂區間 (`from` / `to`) 取得過去歷史價格

### 4. OrderBook (ByHash / ByWallet)
- **`/api/OrderBook/Hash/<network>/<hash_address>`**  
  - 透過交易 hash 取得 OrderBook 資訊  
- **`/api/OrderBook/Wallet/<network>/<wallet_address>`**  
  - 透過 wallet address 取得 OrderBook 資訊

### 5. NFT (by address)
- **`/api/NFT/<wallet_address>`**  
  - 呼叫 `nft/v2/byaddress`，支援多鏈  
  - 回傳結構為 `{ "NFT名稱": "NFT圖片URL", ... }`

### 6. GasPrice
- **`/api/GasPrice/<network>`**  
  - 取得該鏈目前的 Gas 價格資訊

### 7. Data 範例
- **`/api/data`**  
  - 最簡單的測試端點，回傳範例 JSON: `{"id":1,"name":"Alice","message":"Hello from Python backend"}`

---

## 快取機制

- 使用一個名為 `combined_balance_cache` 的 **全域字典**，針對部分 API (如 `get_CombinedBalance`) 做**簡易記憶體快取**。  
- **TTL** (Time-To-Live) 預設設定為 `CACHE_TTL_SECONDS = 12000` 秒 (約 3.3 小時)；可依需求調整  
- 若查到快取且未超過 TTL，就直接回傳，否則才呼叫 1inch API。

> **注意**：此記憶體快取在 **單一後端實例** 下可運作；若要多台後端或更可靠快取方案，可考慮 Redis 等外部服務。

---

## 其他注意事項

1. **CORS**  
   - 透過 `Flask-Cors`，並在程式中使用 `CORS(app)` 或 `@cross_origin()`，可允許前端跨域呼叫。  
2. **節流 / Rate Limit**  
   - 部分程式中 `time.sleep(0.5)`，以減少在同一時間內大量呼叫 1inch API。  
   - 若要更全面的限速，可考慮結合 [Flask-Limiter](https://pypi.org/project/Flask-Limiter/)。  
3. **API Key 保護**  
   - 需在 `.env` 中放置 `1INCH_API_KEY`，並**勿**上傳此金鑰到公開的版本庫。  
4. **網路對應**  
   - `CHAIN_IDS` 定義了常見鏈對應的 chainId (數字)，可依需求擴增或修正。

---

## License

本專案以 MIT License 釋出，詳細條款請參考 [LICENSE](LICENSE) 文件（如無該檔，可自行添加）。

如果有任何問題或想法，歡迎建立 Issue 或 Pull Request！感謝您的使用。

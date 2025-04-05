from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import time

# 或是指定 .env 的路徑：
# load_dotenv(dotenv_path='/path/to/your/.env')
load_dotenv()
my_1inch_api_key = os.getenv("1INCH_API_KEY")
my_wallet_address = os.getenv("WALLET_ADDRESS")

app = Flask(__name__)
CORS(app)

# 定義網絡名稱與對應的 ChainID (全部以十進位字串表示)
CHAIN_IDS = {
    "rabbithole": "1",  # RabbitHole (Ethereum)
    "aurora": "1313161554",  # Aurora
    "arbitrum": "42161",  # Arbitrum
    "avalanche": "43114",  # Avalanche Network
    "base": "8453",  # Base Mainnet (Coinbase)
    "linea": "59144",  # Linea Mainnet
    "binance": "56",  # Binance Smart Chain (BSC)
    "fantom": "250",  # Fantom Opera
    "gnosis": "100",  # Gnosis Chain (0x64 -> 100)
    "kaia": "8217",  # Kaia Mainnet
    "optimistic": "10",  # Optimistic Ethereum
    "polygon": "137",  # Polygon
    "zksync": "324",  # zkSync Era
    "ethereum": "1"  # Ethereum
}


# example
@app.route('/api/data', methods=['GET'])
def get_data():
    # 這裡可以是你從資料庫或其他外部服務取得的資料
    example_data = {
        "id": 1,
        "name": "Alice",
        "message": "Hello from Python backend"
    }
    return jsonify(example_data)


@app.route('/api/OrderBook/Hash/<network>/<hash_address>', methods=['GET'])
def get_OrderBookByHash(hash_address, network):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/orderbook/v4.0/{chain_id}/order/{hash_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {}
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


@app.route('/api/OrderBook/Wallet/<network>/<wallet_address>', methods=['GET'])
def get_OrderBookByWallet(wallet_address, network):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/orderbook/v4.0/{chain_id}/address/{wallet_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {
            "limit": "5"
        }
    }

    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


@app.route('/api/Token/TokenBalance/<network>/<wallet_address>', methods=['GET'])
def get_TokenBalance(wallet_address, network):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/balance/v1.2/{chain_id}/balances/{wallet_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {}
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


@app.route('/api/Token/TokenInfo/<network>/<token_address>', methods=['GET'])
def get_TokenInfo(network, token_address):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/token/v1.2/{chain_id}/custom/{token_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {}
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


@app.route('/api/Token/CombinedBalance/<network>/<wallet_address>', methods=['GET'])
def get_CombinedBalance(network, wallet_address):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    if not chain_id:
        return jsonify({"error": f"無效的網絡名稱：{network}"}), 400

    # ========== (1) 先取得錢包上的所有 Token 與餘額 ==========
    balance_api_url = f"https://api.1inch.dev/balance/v1.2/{chain_id}/balances/{wallet_address}"
    request_options = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {}
    }

    headers = request_options.get("headers", {})
    params = request_options.get("params", {})

    balance_res = requests.get(balance_api_url, headers=headers, params=params).json()
    # balance_res 的結構可能是：
    # {
    #   "0x00a35fd824c717879bf370e70ac6868b95870dfb": "0",
    #   "0x0994206dfe8de6ec6920ff4d779b0d950605fb53": "1000000000000000000",
    #   ...
    # }

    if not isinstance(balance_res, dict):
        # 如果取得資料不是預期的 dict 結構，就直接回傳錯誤
        return jsonify({"error": "取得錢包餘額時發生異常"}), 500
    # if len(balance_res) == 0:
    #     # 如果該錢包沒有持有任何 Token，直接回傳空
    #     return jsonify({})

    token_addresses = list(balance_res.keys())
    # ========== (2) 呼叫 1inch Price API 一次抓所有 Token 的價格 (USD) ==========
    # 參考 1inch 文件，可用「?tokens=0x...,0x...,0x...」一次帶多個地址
    print(token_addresses)
    joined_tokens = ",".join(token_addresses)
    print(joined_tokens)
    price_api_url = f"https://api.1inch.dev/price/v1.1/{chain_id}/?tokens={joined_tokens}"
    price_res = requests.get(price_api_url, headers=headers).json()
    # price_res 結構可能類似：
    # {
    #   "tokens": {
    #     "0x00a35fd824c717879bf370e70ac6868b95870dfb": { "price": "0.23", "decimals": 18, ... },
    #     "0x0994206dfe8de6ec6920ff4d779b0d950605fb53": { "price": "1.02", "decimals": 18, ... },
    #     ...
    #   }
    # }

    token_price_map = {}
    if isinstance(price_res, dict) and "tokens" in price_res:
        token_price_map = price_res["tokens"]  # key: 合約地址(小寫), value: { "price": "...", ... }

    # ========== (3) 逐一取得 Token 名稱 (name) / Symbol / Decimals 等 (可省略) ==========
    #   - 1inch Token Info API: https://api.1inch.dev/token/v1.2/{chain_id}/custom/{token_address}
    #   - 若有大量 token，這裡要小心呼叫次數過多；可依需求做快取或批次查詢。

    combined_result = {}
    for token_addr in token_addresses:
        time.sleep(1)  # <--- 加上這行，每次查詢前先暫停 1 秒，限制頻率
        raw_balance_str = balance_res[token_addr]  # 字串格式的餘額, ex: "1000000000000000000"
        # 預設顯示餘額 = 0
        real_balance = 0
        try:
            # 轉成 int
            real_balance = int(raw_balance_str)
        except ValueError:
            real_balance = 0

        # 取得該 Token 的價格資訊
        token_price_info = token_price_map.get(token_addr.lower(), {})
        price_usd_str = token_price_info.get("price", "0")
        decimals_in_price = token_price_info.get("decimals", 18)

        try:
            price_usd = float(price_usd_str)
        except ValueError:
            price_usd = 0

        # 先呼叫 Token Info API 取得 name
        token_info_url = f"https://api.1inch.dev/token/v1.2/{chain_id}/custom/{token_addr}"
        token_info_res = requests.get(token_info_url, headers=headers).json()
        token_name = token_info_res.get("name", "Unknown")
        token_symbol = token_info_res.get("symbol", "")
        token_decimals = token_info_res.get("decimals", 18)

        # 真實餘額數量
        true_balance_amount = real_balance / (10 ** token_decimals)
        balance_in_usd = true_balance_amount * price_usd
        balance_display_str = f"{true_balance_amount}(USD={balance_in_usd:.2f})"

        final_key = f"{token_addr} ({token_name})"
        combined_result[final_key] = balance_display_str

    # (4) 回傳最終結果
    return jsonify(combined_result)


@app.route('/api/GasPrice/<network>', methods=['GET'])
def get_GasPrice(network):
    # 轉成小寫處理，避免大小寫不一致問題
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    if chain_id is None:
        # 找不到對應的 chain_id 時，回傳錯誤訊息
        return jsonify({"error": f"無效的網絡名稱：{network}"}), 400

    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {}
    }
    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    apiUrl = "https://api.1inch.dev/gas-price/v1.5/" + chain_id

    return requests.get(apiUrl, headers=headers, params=params).json()

if __name__ == '__main__':
    app.run(debug=True)

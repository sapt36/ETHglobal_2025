from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
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

# 建立一個簡易的 in-memory cache, 結構可自行調整
# 格式: { cache_key: {"data":..., "timestamp":...} }
combined_balance_cache = {}

CACHE_TTL_SECONDS = 12000  # 資料緩存時間 (秒)，可自行調整

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


@app.route('/api/Chart/Token/<network>/<token_address>', methods=['GET'])
def get_ChartToken(network, token_address):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/token-details/v1.0/charts/interval/{chain_id}/{token_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {
            "interval": "24h, 1w, 1m, 1y",
            "from_time": "1631644261"
        }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


# example
# interval = 24h, 1w, 1m, 1y
@app.route('/api/Chart/NaiveChain/<network>', methods=['GET'])
def get_ChartNaiveChain(network):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/token-details/v1.0/charts/interval/{chain_id}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {
            "interval": "24h, 7d, 30d, 365d",
            "from_time": "1631644261"
        }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


# example
# V_GOD Token : MOO DENG -> 0x28561b8a2360f463011c16b6cc0b0cbef8dbbcad
# "from": "1743844261" 2025/04/05 17:11:01
# "to": "1743854275"   2025/04/05 19:57:55
@app.route('/api/Chart/HistoryTokenPrice/<network>/<TimeFrom>/<TimeTo>/<token_address>', methods=['GET'])
def get_HistoryTokenPrice(network, token_address, TimeFrom, TimeTo):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    apiUrl = f"https://api.1inch.dev/token-details/v1.0/charts/range/{chain_id}/{token_address}"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {
            "from": f"{TimeFrom}",
            "to": f"{TimeTo}",
        }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    return requests.get(apiUrl, headers=headers, params=params).json()


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
@cross_origin()
def get_CombinedBalance(network, wallet_address):
    network_key = network.lower()
    chain_id = CHAIN_IDS.get(network_key)

    if not chain_id:
        return jsonify({"error": f"無效的網絡名稱：{network}"}), 400

    # --- Step 1: 檢查快取
    cache_key = f"{network_key}_{wallet_address}"
    cache_entry = combined_balance_cache.get(cache_key)

    # 若有快取，且未超過設定的 TTL，就直接回傳快取結果
    if cache_entry:
        cached_time = cache_entry["timestamp"]
        if (time.time() - cached_time) < CACHE_TTL_SECONDS:
            return jsonify(cache_entry["data"])  # 直接回傳快取資料

    # --- Step 2: 若沒有可用快取，就呼叫外部 API
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
    if not isinstance(balance_res, dict):
        return jsonify({"error": "取得錢包餘額時發生異常"}), 500

    token_addresses = list(balance_res.keys())

    # (3) 取得 Token Metadata 並計算
    combined_result = {}
    for token_addr in token_addresses:
        time.sleep(0.5)  # 節流 - 每查一個 token 前暫停 1 秒
        raw_balance_str = balance_res[token_addr]
        try:
            real_balance = int(raw_balance_str)
        except ValueError:
            real_balance = 0

        # 先呼叫 1inch Token Info API
        token_info_url = f"https://api.1inch.dev/token/v1.2/{chain_id}/custom/{token_addr}"
        token_info_res = requests.get(token_info_url, headers=headers).json()
        token_name = token_info_res.get("name", "Unknown")
        token_decimals = token_info_res.get("decimals", 18)
        token_img_url = token_info_res.get("logoURI", "Unknown")

        true_balance_amount = real_balance / (10 ** token_decimals)
        balance_display_str = f"[{true_balance_amount}, {token_img_url}]"

        final_key = f"{token_name}"
        combined_result[final_key] = balance_display_str

    # --- Step 3: 把結果存進快取
    combined_balance_cache[cache_key] = {
        "data": combined_result,
        "timestamp": time.time()
    }

    return jsonify(combined_result)


@app.route('/api/NFT/<wallet_address>', methods=['GET'])
def get_NFTs(wallet_address):
    apiUrl = "https://api.1inch.dev/nft/v2/byaddress"
    requestOptions = {
        "headers": {
            "Authorization": f"Bearer {my_1inch_api_key}"
        },
        "body": "",
        "params": {
            "chainIds": [1, 137, 8453, 42161, 8217, 43114, 10],
            "address": f"{wallet_address}"
        }
    }
    headers = requestOptions.get("headers", {})
    params = requestOptions.get("params", {})

    # 呼叫 1inch API
    raw_res = requests.get(apiUrl, headers=headers, params=params).json()
    # raw_res 可能包含結構：
    # {
    #   "assets": [
    #       {
    #         "name": "...",
    #         "image_url": "...",
    #         ...
    #       },
    #       ...
    #   ]
    # }

    # 取出 assets 陣列 (如果不存在，預設空陣列)
    assets = raw_res.get("assets", [])

    # 準備要回傳的資料結構：{"NFT名稱": "NFT圖片URL", ...}
    result = {}

    for item in assets:
        nft_name = item.get("name") or "Unknown"
        nft_image_url = item.get("image_url") or "No Image"

        # 將 name : image_url 放入字典
        result[nft_name] = nft_image_url

    # 最終將組合後的 result 回傳
    return jsonify(result)


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

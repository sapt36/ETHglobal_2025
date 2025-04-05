from math import degrees

from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import requests

# 或是指定 .env 的路徑：
# load_dotenv(dotenv_path='/path/to/your/.env')
load_dotenv()
my_1inch_api_key = os.getenv("1INCH_API_KEY")
my_wallet_address = os.getenv("WALLET_ADDRESS")

app = Flask(__name__)

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


@app.route('/api/TokenBalance/<network>/<wallet_address>', methods=['GET'])
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

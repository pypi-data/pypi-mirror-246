import json
import os
import time
from decimal import *
from typing import Optional

import requests
from Crypto.Hash import keccak
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from web3 import HTTPProvider, Web3
from web3.middleware import construct_sign_and_send_raw_middleware


class Client:
    BACKEND_API_URL = 'https://api.aark.digital'
    PRICE_API_URL = 'https://price-api.aark.digital'
    REQUEST_TIMEOUT: Decimal = 10
    DEFAULT_RPC_URL = 'https://arb1.arbitrum.io/rpc'
    OCT_ROUTER_CONTRACT_ADDRESS = "0x4213d42A5A6Bd38Ef9A166b179D1f360FF536D39"
    READER_CONTRACT_ADDRESS = "0x0A2e171DB1748Cab3F1549Cf12096546374346ac"
    ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
    QTY_DECIMALS = 10
    PRICE_DECIMALS = 8

    def __init__(
        self, private_key: str, rpc_url: str = DEFAULT_RPC_URL
    ):
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.w3 = Web3(HTTPProvider(self.rpc_url))
        self.wallet: LocalAccount = Account.from_key(self.private_key)
        self.max_oracle_id = 0
        self.w3.middleware_onion.add(
            construct_sign_and_send_raw_middleware(self.wallet))
        getcontext().prec = 18
        self.__save_oracle_ids()

        with open(f"{os.path.dirname(__file__)}/abis/OctRouter.json") as f:
            abi = json.load(f)['abi']
            self.oct_router_contract = self.w3.eth.contract(
                address=self.OCT_ROUTER_CONTRACT_ADDRESS, abi=abi)

        with open(f"{os.path.dirname(__file__)}/abis/ContractReader.json") as f:
            abi = json.load(f)['abi']
            self.reader_contract = self.w3.eth.contract(
                address=self.READER_CONTRACT_ADDRESS, abi=abi
            )

    def order(self, qty: Decimal, symbol: str, is_long: bool, is_limit: bool = False, price: Decimal = 0, slippage_tolerance: Decimal = 0, trigger_price: Decimal = 0):
        is_reduce_only = False
        market_id = self.__convert_symbol_to_id(symbol)
        nonce = int(time.time() * 1000)
        order_object = self.__get_order_object(
            qty, price, slippage_tolerance, market_id, is_long, is_limit, int(nonce/1000), is_reduce_only)
        if trigger_price:
            return self.__trigger_order(symbol, order_object,
                                        nonce, trigger_price, is_limit)
        else:
            return self.__order(order_object, nonce)

    def cancel_limit_order(self, order_id: int):
        nonce = int(time.time() * 1000)

        msg_hash = keccak.new(
            digest_bits=256).update(encode(['address', 'uint256', 'uint256'], [
                self.wallet.address, order_id, nonce])).hexdigest()

        signature = self.w3.eth.account.sign_message(
            encode_defunct(hexstr=msg_hash), private_key=self.private_key)

        headers = {
            "signature": signature.signature.hex()
        }
        data = {
            "delegator": self.wallet.address,
            "delegatee": self.wallet.address,
            "orderId": order_id,
            "nonce": nonce
        }

        response = requests.post(
            f"{self.BACKEND_API_URL}/oct/cancel-limit-order", json=data, headers=headers)

        if response.json()["code"] == 200:
            return True
        else:
            return False

    def cancel_trigger_order(self, nonce: int, trigger_price: Decimal):
        msg_hash = keccak.new(
            digest_bits=256).update(encode(['address', 'uint256'], [
                self.wallet.address, int(nonce)])).hexdigest()
        signature = self.w3.eth.account.sign_message(
            encode_defunct(hexstr=msg_hash), private_key=self.private_key)

        headers = {
            "signature": signature.signature.hex()
        }
        data = {
            "delegator": self.wallet.address,
            "delegatee": self.wallet.address,
            "nonce": nonce,
            "price": trigger_price
        }

        response = requests.post(
            f"{self.BACKEND_API_URL}/oct/disable-nonce", json=data, headers=headers)

        if response.json()["code"] == 200:
            return True
        else:
            return False

    def get_futures_status(self):
        status = self.reader_contract.functions.getUserFuturesStatusWithPrice(
            self.wallet.address, self.__get_index_price_array()).call()
        positions = []
        collaterals = []

        for i in range(0, len(status[0])):
            if (status[0][i][0] != 0):
                positions.append({
                    "market": self.symbols[i],
                    "qty": Decimal(status[0][i][0])/(10 ** 10),
                    "entry_price": Decimal(status[0][i][2])/(10**8),
                })
        for i in range(0, len(status[1])):
            if status[1][i][0] != self.ZERO_ADDRESS:
                collaterals.append({
                    "token_address": status[1][i][0],
                    "qty": Decimal(status[1][i][1]) / (10 ** 10),
                    "withdrawable": Decimal(status[1][i][2]) / (10 ** 10),
                })

        return {
            "positions": positions,
            "collaterals": collaterals,
            "account_value": Decimal(status[2]) / (10 ** 18),
            "weighted_balance": Decimal(status[4]) / (10 ** 18),
            "free": (Decimal(status[4]) - Decimal(status[8])) / (10 ** 18),
            "pending_funding_fee": Decimal(status[7]) / (10 ** 18),
            "initial_margin": Decimal(status[8]) / (10 ** 18),
            "maintenance_margin": Decimal(status[9]) / (10 ** 18)
        }

    def get_limit_orders(self, symbol: Optional[str]):
        response = requests.get(
            f"{self.BACKEND_API_URL}/order/futures/limit?status=0&user={self.wallet.address}{'&marketId='+ str(self.__convert_symbol_to_id(symbol)) if symbol else ''}")
        return response.json()['data']

    def get_trigger_orders(self):
        response = requests.get(
            f"{self.BACKEND_API_URL}/oct/trigger-order?user={self.wallet.address}")
        return response.json()['data']

    def get_markets(self):
        status = self.reader_contract.functions.getMarkets().call()
        prices = self.__get_index_prices()
        markets = {}
        for i in range(0, len(status)):
            if (status[i][7] != 0):
                symbol = self.__convert_id_to_symbol(i)
                mark_price = Decimal(prices[symbol]['indexPrice']) * (Decimal(1) + (
                    Decimal(status[i][2]) / Decimal(status[i][4])) * Decimal(0.01))
                funding_rate = (
                    Decimal(status[i][1]) / ((10 ** 18) * mark_price)) * 100 * 3600
                markets[self.__convert_id_to_symbol(i)] = {
                    'symbol': symbol,
                    'acc_funding_factor': Decimal(status[i][0]),
                    'funding_rate': funding_rate,
                    'skewness': Decimal(status[i][2]) / (10 ** self.QTY_DECIMALS),
                    'depth_factor': Decimal(status[i][4] / (10 ** self.QTY_DECIMALS)),
                    'cap': Decimal(status[i][5]) / (10 ** self.QTY_DECIMALS),
                    'index_price': prices[symbol]['indexPrice'],
                    'mark_price': mark_price,
                    'spread': (Decimal(prices[symbol]['spread']) * (10 ** 5)).__round__() / (10 ** 3)
                }
        return markets

    def __order(self, order_object: str, nonce: int):
        msg_hash = keccak.new(
            digest_bits=256).update(encode(['address', 'uint256', 'uint256'], [
                self.wallet.address, int(order_object, 16), nonce])).hexdigest()

        signature = self.w3.eth.account.sign_message(
            encode_defunct(hexstr=msg_hash), private_key=self.private_key)

        headers = {
            "signature": signature.signature.hex()
        }
        data = {
            "delegator": self.wallet.address,
            "delegatee": self.wallet.address,
            "order": order_object,
            "nonce": nonce
        }

        response = requests.post(
            f"{self.BACKEND_API_URL}/oct/order", json=data, headers=headers)

        if response.json()["code"] == 200:
            return True
        else:
            return False

    def __trigger_order(self, symbol: str, order_object: str, nonce: Decimal,  trigger_price: Decimal, is_limit: bool):
        current_price = (Decimal(self.__get_index_price(symbol)[
                         'indexPrice']) * (10 ** self.PRICE_DECIMALS)).__floor__()
        trigger_price_applied_decimals = (
            Decimal(trigger_price) * (10 ** self.PRICE_DECIMALS)).__floor__()
        msg_hash = keccak.new(
            digest_bits=256).update(encode(['address', 'uint256', 'uint256', 'uint256', 'uint256'], [
                self.wallet.address, int(order_object, 16), current_price, trigger_price_applied_decimals, nonce])).hexdigest()

        signature = self.w3.eth.account.sign_message(
            encode_defunct(hexstr=msg_hash), private_key=self.private_key)

        headers = {
            "signature": signature.signature.hex()
        }
        data = {
            "delegator": self.wallet.address,
            "delegatee": self.wallet.address,
            "order": order_object,
            "nonce": nonce,
            "orderPrice": current_price,
            "triggerPrice": trigger_price_applied_decimals,
            "orderType": "stopLimit" if is_limit else "stopMarket",
        }

        response = requests.post(
            f"{self.BACKEND_API_URL}/oct/trigger-order", json=data, headers=headers)

        if response.json()["code"] == 200:
            return True
        else:
            return False

    def __get_order_object(self, qty: Decimal, price: Decimal, slippage_tolerance: Decimal, market_id: int, is_long: bool, is_limit: bool, timestamp: int, is_reduce_only: bool):
        return format(int(format(is_reduce_only, "01b") + format(timestamp, "032b") + format(is_limit, "01b") + format(is_long, "01b")
                          + format(market_id, "08b") + format(int(slippage_tolerance *
                                                                  (10 ** self.PRICE_DECIMALS)), "054b")
                          + format(int(price * (10 ** self.PRICE_DECIMALS)), "054b") +
                          format(int(qty * (10 ** self.QTY_DECIMALS)), "057b"), 2), '#046x')

    def __get_epoch(self):
        return ((time.time()) / (3*24*3600)).__floor__()

    def __get_market_list(self):
        response = requests.get(f"{self.BACKEND_API_URL}/markets")
        return response.json()['data']

    def __get_index_price(self, symbol: str):
        return self.__get_index_prices()[symbol]

    def __get_index_prices(self):
        response = requests.get(f"{self.PRICE_API_URL}/price/all")
        return response.json()

    def __save_oracle_ids(self):
        response = requests.get(f"{self.BACKEND_API_URL}/markets/ids")
        self.oracle_ids = response.json()['data']
        self.symbols = {}
        for id in self.oracle_ids:
            self.symbols[self.oracle_ids[id]] = id
            self.max_oracle_id = max(self.max_oracle_id, self.oracle_ids[id])

    def __convert_symbol_to_id(self, symbol: str):
        if symbol not in self.oracle_ids:
            self.__save_oracle_ids()
        return self.oracle_ids[symbol]

    def __convert_id_to_symbol(self, id: int):
        if id not in self.symbols:
            self.__save_oracle_ids()
        return self.symbols[id]

    def __get_index_price_array(self):
        prices = [100000000]
        index_prices = self.__get_index_prices()

        # Temporal Way
        index_prices["FRAX"] = {
            'indexPrice': 1
        }

        for i in range(1, self.max_oracle_id + 1):
            prices.append(Decimal(index_prices[self.__convert_id_to_symbol(
                i)]['indexPrice'] * (10 ** self.PRICE_DECIMALS)).__floor__())
        return prices

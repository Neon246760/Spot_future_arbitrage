import time
import ccxt
from typing import Literal

from config import BINANCE_CONFIG


exchange = ccxt.binance(BINANCE_CONFIG)


def spot_place_order(buy_or_sell: Literal['BUY', 'SELL'], price, quantity, symbol):
    """
    现货下单函数
    :param buy_or_sell: 枚举类型，支持参数 'BUY' 或 'SELL'
    :param price: 下单价格
    :param quantity: 下单数量
    :param symbol: 进行交易的交易对
    :return: 订单信息
    """
    params = {
        'symbol': symbol,
        'side': buy_or_sell,
        'type': 'LIMIT',
        'quantity': quantity,
        'price': price,
        'timeInForce': 'GTC',
        'timestamp': int(time.time()) * 1000
    }
    for i in range(5):
        try:
            if buy_or_sell == 'BUY' or buy_or_sell == 'SELL':
                order_info = exchange.private_post_order(params=params)
            else:
                raise ValueError("buy_or_sell只能是：'BUY' 或 'SELL'")

            print('✅ 现货下单成功！订单信息为：\n', order_info)
            return order_info

        except Exception as e:
            print('⭕ 现货下单报错，1s后重试', e)
            time.sleep(1)

    print('❌ 现货下单报错次数过多，程序终止！')
    exit()


def account_transfer(amount, from_account, to_account, asset):
    """
    现货账户与币本位账户间的划转函数
    :param amount: 划转的数量
    :param from_account: 转出账户，只能填 'SPOT' 或 'CONTRACT'
    :param to_account: 转入账户，只能填 'SPOT' 或 'CONTRACT'
    :param asset: 需要划转的资产
    :return: 划转信息
    """
    if from_account == 'SPOT' and to_account == 'CONTRACT':
        transfer_type = 'MAIN_CMFUTURE'
    elif from_account == 'CONTRACT' and to_account == 'SPOT':
        transfer_type = 'CMFUTURE_MAIN'
    else:
        raise ValueError("from_account和to_account只能是：'SPOT' 或 'CONTRACT'")

    params = {
        'type': transfer_type,
        'asset': asset,
        'amount': amount
    }

    for i in range(5):
        try:
            params['timestamp'] = int(time.time()) * 1000
            transfer_info = exchange.sapi_post_asset_transfer(params=params)
            print('✅ 转账成功：', from_account, 'to', to_account, amount)
            print('✉️ 转账信息：', transfer_info, '\n')
            return transfer_info
        except Exception as e:
            print('⭕ 转账报错，1s后重试', e)
            time.sleep(1)

    print('❌ 转账报错次数过多，程序终止')
    exit()


def contract_place_short_order(open_or_close: Literal['OPEN', 'CLOSE'], price: float, quantity: float, symbol: str):
    """
    用于开空单或平空单的函数
    :param symbol: 合约代码，如'BTCUSD_250328'
    :param open_or_close: 开空单或平空单，只能填 'OPEN' 或 'CLOSE'
    :param price: 做空价格
    :param quantity: 做空的合约数量
    :return:
    """
    if open_or_close == 'OPEN':
        side = 'SELL'
    elif open_or_close == 'CLOSE':
        side = 'BUY'
    else:
        raise ValueError("open_or_close只能是：'OPEN' 或 'CLOSE'")

    params = {
        'side': side,
        'positionSide': 'SHORT',
        'symbol': symbol,
        'type': 'LIMIT',
        'price': price,
        'quantity': quantity,
        'timeInForce': 'GTC'
    }

    for i in range(5):
        try:
            params['timestamp'] = int(time.time() * 1000)
            order_info = exchange.dapiprivate_post_order(params)
            print('✅ 币安合约交易下单成功：', symbol, open_or_close, price, quantity)
            print('✉️ 下单信息：', order_info, '\n')
            return order_info
        except Exception as e:
            print('⭕ 币安合约交易下单报错，1s后重试...', e)
            time.sleep(1)

    print('❌ 币安合约交易下单报错次数过多，程序终止')
    exit()


def get_arbitrage_symbols() -> list:
    """
    返回一个存有可以进行期现套利的币种的列表
    :return: 一个存有可以进行期现套利的币种的列表
    """
    response = exchange.dapipublic_get_exchangeinfo()['symbols']
    symbols_list = [d['pair'][:-3] for d in response if d['contractType'] == 'CURRENT_QUARTER']

    return symbols_list
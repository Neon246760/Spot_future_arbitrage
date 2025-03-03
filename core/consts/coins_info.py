from config import *
from core.utils.binance import exchange
from core.utils.commons import count_decimal_places


spot_name = coin + 'USDT'  # 现货交易对
contract_name = coin + 'USD_' +contract_date  # 币本位合约交易对

contract_size = 100 if coin == 'BTC' else 10  # 合约乘数

# 获取币本位合约价格精度
response = exchange.dapipublic_get_exchangeinfo()['symbols']
coin_precision = int([d['pricePrecision'] for d in response if d['baseAsset'] == coin][0])

# 获取现货交易价格精度和最小下单量精度
response = exchange.public_get_exchangeinfo(params={'symbol': spot_name})['symbols'][0]['filters']
spot_price_precision = 0
spot_Qty_precision = 0
for d in response:
    if d['filterType'] == 'PRICE_FILTER':
        spot_price_precision = count_decimal_places(d['minPrice'])  # 价格精度
    elif d['filterType'] == 'LOT_SIZE':
        spot_Qty_precision = count_decimal_places(d['minQty'])  # 最小下单量精度
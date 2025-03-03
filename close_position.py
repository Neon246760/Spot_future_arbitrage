from core.utils.binance import *
from core.consts.coins_info import *
from core.utils.commons import round_down


spot_price = 0
position_amount = 0

if __name__ == '__main__':
    execute_num = int(execute_usdt / contract_size)

    positions = exchange.dapiprivate_get_account(params={'timestamp': int(time.time()) * 1000})['positions']
    for d in positions:  # 将合约按计划逐笔平仓
        if d['symbol'] == contract_name and d['positionSide'] == 'SHORT':
            position_amount = float(d['positionAmt']) * -1

    # Step1. 平仓币本位合约空单
    print('\n', '*' * 40, 'Step1: 平仓合约', '*' * 40)
    while position_amount > 0:
        spot_price = float(exchange.public_get_ticker_bookticker(params={'symbol': spot_name})['bidPrice'])  # 获取现货买一价
        contract_price = float(exchange.dapipublic_get_ticker_bookticker(params={'symbol': contract_name})[0]['askPrice'])  # 获取合约卖一价

        spreads = contract_price / spot_price - 1  # 计算价差
        print('🔔 目前现货价格为：%.4f，期货价格为：%.4f，价差为：%.4f%%' % (spot_price, contract_price, spreads * 100))

        if spreads < close_threshold:
            print('▶️ 价差小于平仓阈值，准备平仓')

            price = contract_price * 1.02
            price = round_down(price, coin_precision)

            contract_place_short_order(open_or_close='CLOSE', price=price, quantity=min(position_amount, execute_num),
                                       symbol=contract_name)
            position_amount -= execute_num
        else:
            print('⏸️ 价差大于目标阀值，不平仓')

        # 循环结束
        print('=' * 60, '本次循环结束，暂停2s', '=' * 60, '\n')
        time.sleep(2)

    # Step2: 将卖得的货币转入现货账户
    print('\n', '*' * 40, 'Step2: 划转', '*' * 40)
    balance = exchange.dapiprivate_get_account(params={'timestamp': int(time.time()) * 1000})['assets']
    num = [d['walletBalance'] for d in balance if d['asset'] == coin][0]  # 注意：程序会将币本位账户中所有该币种都转走
    print(f'🌀 待划转的{coin}数量为 {num}')
    account_transfer(amount=num, from_account='CONTRACT', to_account='SPOT', asset=coin)

    # Step3: 在现货账户将币种换为USDT
    print('\n', '*' * 40, 'Step3: 卖出现货', '*' * 40)
    balance = exchange.private_get_account(params={'timestamp': int(time.time()) * 1000})['balances']
    num = round_down(float([d['free'] for d in balance if d['asset'] == coin][0]), spot_Qty_precision)
    spot_price = float(exchange.public_get_ticker_bookticker(params={'symbol': spot_name})['bidPrice'])
    spot_order_info = spot_place_order(buy_or_sell='SELL', price=round_down(spot_price * 0.98, spot_price_precision),
                                       quantity=num, symbol=spot_name)

    print('✅ 完成平仓计划，退出程序')


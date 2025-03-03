from core.utils.binance import *
from core.consts.coins_info import *
from core.utils.commons import round_down


count = 0

if __name__ == '__main__':
    while True:
        spot_price = float(exchange.public_get_ticker_bookticker(params={'symbol': spot_name})['askPrice'])  # 获取现货卖一价
        contract_price = float(exchange.dapipublic_get_ticker_bookticker(params={'symbol': contract_name})[0]['bidPrice'])  # 获取期货买一价

        spreads = contract_price / spot_price - 1  # 计算价差
        print('🔔 目前现货价格为：%.4f，期货价格为：%.4f，价差为：%.4f%%' % (spot_price, contract_price, spreads * 100))

        if spreads > open_threshold:
            print('▶️ 价差大于开仓阈值，准备建仓')

            # 计算做空合约的数量
            execute_num = int(execute_usdt / contract_size)
            coin_num = execute_num * contract_size / contract_price
            short_contract_fee = coin_num * contract_fee_rate

            # 计算买入现货的数量
            # buy_spot_num * (1 - spot_fee_rate) - sell_contract_fee = sell_coin_num
            buy_coin_num = round_down((coin_num + short_contract_fee) / (1 - spot_fee_rate), spot_Qty_precision)

            print(f'🌀 计划做空 {execute_num} 张合约，对应 {coin_num} 个{coin}，'
                  f'合约手续费为 {short_contract_fee}，需要买入现货{coin} {buy_coin_num} 个')

            # Step1: 买入现货
            print('\n', '*' * 40, 'Step1: 买入现货', '*' * 40)
            price = round_down(spot_price * 1.02, spot_price_precision)
            spot_order_info = spot_place_order(buy_or_sell='BUY', price=price, quantity=buy_coin_num, symbol=spot_name)


            # Step2: 将买入的现货转入币本位合约账户
            print('\n', '*' * 40, 'Step2: 划转', '*' * 40)
            balance = exchange.private_get_account(params={'timestamp': int(time.time()) * 1000 })['balances']
            num = [d['free'] for d in balance if d['asset'] == coin][0]  # 注意：程序会将现货账户中所有该币种都转走
            print(f'🌀 待划转的{coin}数量为 {num}')
            account_transfer(amount=num, from_account='SPOT', to_account='CONTRACT', asset=coin)

            # Step3: 做空合约
            print('\n', '*' * 40, 'Step3: 做空合约', '*' * 40)
            price = contract_price * 0.98
            price = round_down(price, coin_precision)
            contract_order_info = contract_place_short_order(open_or_close='OPEN', price=price, quantity=execute_num,
                                                             symbol=contract_name)

            print('✉️ 现货下单信息为：', spot_order_info, '\n')
            print('✉️ 合约下单信息为：', contract_order_info, '\n')

            count += 1

        else:
            print('⏸️ 价差小于目标阀值，不建仓')


        # 循环结束
        print('=' * 60, '本次循环结束，暂停2s', '=' * 60, '\n')
        time.sleep(2)

        # 是否退出循环
        if count >= max_count:
            print('✅ 达到最大下单次数，完成建仓计划，退出程序')
            break
import time
import warnings
import pandas as pd
import dataframe_image as dfi

from core.utils.wechat import *
from config import monit_interval
from core.utils.log_kit import MyLogger
from core.utils.commons import ClosingDateGetter, Sleeper
from core.utils.binance import exchange, get_arbitrage_symbols


warnings.filterwarnings('ignore')
pd.set_option('expand_frame_repr', False)
logger = MyLogger('monitor').get_logger()


symbols_list = get_arbitrage_symbols()
date_list = ClosingDateGetter.get_closing_dates()

is_debug = True


def main():
    logger.warning(f'可以进行期现套利的币种有：{symbols_list}')

    all_data_list = []
    logger.debug(f"{'*' * 40}开始更新数据{'*' * 40}")

    for symbol in symbols_list:
        spot_pair = symbol + 'USDT'
        spot_price = float(exchange.public_get_ticker_bookticker(params={'symbol': spot_pair})['askPrice'])
        data_list = [symbol, spot_price]

        for date in date_list:
            contract_pair = symbol + 'USD_' + date
            contract_price = float(
                exchange.dapipublic_get_ticker_bookticker(params={'symbol': contract_pair})[0]['bidPrice'])
            rate = (contract_price / spot_price) - 1
            rate_pct = str(round(rate * 100, 2)) + '%'
            data_list.extend([contract_pair, contract_price, rate_pct])
            if rate > 0.05:
                send_wechat_msg(f'🔔 {contract_price}的期现套利利润已达{rate_pct}，可以考虑进行套利！')

        all_data_list.append(data_list)
        logger.info(f'{symbol}套利数据已更新')
        time.sleep(0.5)

    logger.ok('套利数据已更新完毕')
    logger.debug(f"{'*' * 40}数据更新完毕{'*' * 40}")
    df = pd.DataFrame(all_data_list)
    df.rename(columns={0: 'symbol', 1: 'spot_price', 2: 'current_quarter_contract', 3: 'Current_Quarter',
                       4: date_list[0], 5: 'next_quarter_contract', 6: 'Next_Quarter',
                       7: date_list[1]}, inplace=True)
    df = df[['symbol', 'spot_price', 'Current_Quarter', 'Next_Quarter', date_list[0], date_list[1]]]
    df.set_index('symbol', inplace=True)
    logger.debug(f'期现套利利差表：\n{df}')

    dfi.export(df, r'.\arbitrage_rate.png', table_conversion='matplotlib')
    send_wechat_img(r'.\arbitrage_rate.png')
    send_wechat_msg('当日期现套利利差表已获取完毕！')

if __name__ == '__main__':
    if is_debug:
        main()
    else:
        while True:
            Sleeper.run_on_periodic_basis(time_interval=monit_interval, func=main)
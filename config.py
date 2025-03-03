proxies = {'http': '127.0.0.1:33210', 'https': '127.0.0.1:33210'}
# proxies = {}
BINANCE_CONFIG = {
    'apiKey': '',
    'secret': '',
    'proxies': proxies
}

# 信息于此处查询：https://www.binance.com/zh-CN/futures/trading-rules/quarterly
coin = 'BTC'.upper()  # 目标币种
contract_date = '250627'

# 最终执行金额 = execute_usdt * max_count
execute_usdt = 500  # 小币填最大500，BTC最大填3000
max_count = 2  # 建仓次数

open_threshold = 0.08  # 建仓价差
close_threshold = 0.01  # 平仓价差

# 手续费设置
spot_fee_rate = 1 / 1000  # 如果用bnb支付手续费，可设置为0。但需要保证自己账户中有足够的bnb
contract_fee_rate = 5 / 10000

# 微信机器人url设置
# wechat_webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='
wechat_webhook_url = ''
# monitor运行周期设置
monit_interval = '24h'
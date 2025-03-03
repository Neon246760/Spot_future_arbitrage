# Spot_future_arbitrage

监控并进行针对币安币本位合约的期现套利

## 目录

- [安装](#安装)
- [使用](#使用)
- [功能](#功能)

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/Neon246760/Spot_future_arbitrage.git
   ```
2. 进入项目目录：
   ```bash
   cd Spot_future_arbitrage
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用

1. 配置您的 API 密钥和秘密：
   在 `config.py` 文件中，填写 `BINANCE_CONFIG` 字典中的 `apiKey` 和 `secret` 字段。

2. 设置代理（可选）：
   如果需要使用代理，请在 `config.py` 中取消注释并设置 `proxies` 字典。

3. 配置交易参数：
   根据您的需求调整 `execute_usdt`、`max_count`、`open_threshold` 和 `close_threshold` 等参数。

4. 运行监控程序：
   ```bash
   python monitor.py
   ```

5. 监控周期设置：
   您可以在 `config.py` 中调整 `monit_interval` 来设置监控的运行周期。

6. 企业微信机器人配置
    请在`wechat_webhook_url`中配置企业微信机器人的url，程序会将每日的套利结果发送给机器人。

7. 开仓阈值
    当决定开仓时，请配置好`open_threshold`，然后运行open_position.py，程序将在大于阈值时开仓
    ```bash
   python open_position.py
   ```

8. 平仓阈值
    当决定平仓时，请配置好`close_threshold`，然后运行close_position.py，程序将在小于阈值时平仓
    ```bash
   python close_position.py
   ```

## 功能

- **监控套利**：`monitor.py` 文件用于监控期现套利机会。
- **平仓程序**：`close_position.py`
- **开仓程序**：`open_position.py`

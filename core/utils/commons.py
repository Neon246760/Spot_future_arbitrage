import time
import datetime


def count_decimal_places(s: str) -> int:
    """
    输入一个字符串格式的小数，返回其小数位数
    :param s: 一个字符串格式的小数
    :return: 小数位数

    案例：
    (s: ‘0.00100000’) ，返回 3
    """
    # 找到小数点的位置
    dot_index = s.find('.')
    if dot_index == -1:
        return 0  # 没有小数点，小数位数为0

    # 取小数点后的部分
    decimal_part = s[dot_index + 1:]

    # 计算小数点后部分的长度，直到遇到非零数字
    for i, char in enumerate(decimal_part):
        if char != '0':
            return i + 1  # 返回小数位数

    return len(decimal_part)  # 如果全是零，返回小数点后部分的长度


def round_down(number, decimals):
    """
    根据精度对数字进行就低不就高处理

    :param number: 数字
    :param decimals: 精度
    :return: 处理后的数字

    案例：
    (number = 3.77 , decimals = 1) , 返回 3.7
    """
    multiplier = 10 ** decimals
    return int(number * multiplier) / multiplier


class Sleeper:
    """使函数按指定周期运行，其余时间休眠"""

    @staticmethod
    def _next_run_time(time_interval):
        """
        根据time_interval，计算下次运行的时间。（只支持分钟和小时）
        :param time_interval: 运行的周期
        :return: 下次运行的时间

        案例：
        15m  当前时间为：12:50:51  返回时间为：13:00:00
        15m  当前时间为：12:39:51  返回时间为：12:45:00

        10m  当前时间为：12:38:51  返回时间为：12:40:00
        10m  当前时间为：12:11:01  返回时间为：12:20:00

        5m  当前时间为：12:33:51  返回时间为：12:35:00
        5m  当前时间为：12:34:51  返回时间为：12:40:00

        30m  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00
        30m  当前时间为：14:37:51  返回时间为：14:56:00

        1h  当前时间为：14:37:51  返回时间为：15:00:00
        """
        # 检测 time_interval 是否配置正确，并将 时间单位 转换成 可以解析的时间单位
        if time_interval.endswith('m') or time_interval.endswith('h'):
            pass
        elif time_interval.endswith('H'):  # 小时兼容使用H配置， 例如  1H  2H
            time_interval = time_interval.replace('H', 'h')
        else:
            print('⚠️ time_interval格式不符合规范，程序退出！')
            exit()

        # 将 time_interval 转换成 时间类型
        value = int(time_interval[:-1])
        ti = datetime.timedelta(minutes=value) if time_interval[-1] == 'm' else datetime.timedelta(hours=value)

        # 获取当前时间
        now_time = datetime.datetime.now()
        # 计算当日时间的 00：00：00
        this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
        # 每次计算时间最小时间单位1分钟
        min_step = datetime.timedelta(minutes=1)
        # 目标时间：设置成默认时间，并将 秒，毫秒 置零
        target_time = now_time.replace(second=0, microsecond=0)

        while True:
            # 增加一个最小时间单位
            target_time = target_time + min_step
            # 获取目标时间已经从当日 00:00:00 走了多少时间
            delta = target_time - this_midnight
            # delta 时间可以整除 time_interval，表明时间是 time_interval 的倍数，是一个 整时整分的时间
            if int(delta.total_seconds()) % int(ti.total_seconds()) == 0:
                break

        return target_time

    @classmethod
    def run_on_periodic_basis(cls, time_interval, func) -> None:
        """
        根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间并运行需要运行的函数
        :param time_interval: 时间周期配置，用于计算下个周期的时间
        :param func: 需要运行的函数
        :return:
        """
        # 计算下次运行时间
        target_time = cls._next_run_time(time_interval)
        # 配置 cheat_seconds ，对目标时间进行 提前 或者 延后
        print(f'⏳程序等待下次运行，下次时间：{target_time}')

        # 开始睡眠，如果计算获得的 run_time 小于 now, sleep就会一直sleep
        _now = datetime.datetime.now()
        if target_time > _now:  # 计算的下个周期时间超过当前时间，直接追加一个时间周期
            time.sleep(max(0, (target_time - _now).seconds))
        while True:  # 在靠近目标时间时
            if datetime.datetime.now() > target_time:
                time.sleep(1)
                break

        # 运行所需函数
        func()
        print('=' * 60, '本轮函数运行完毕', '=' * 60, '\n')


class ClosingDateGetter:
    """用于获取合约交割日期。"""

    @staticmethod
    def _get_last_fridays(start_year: int) -> list:
        """
        获取指定年份中3月、6月、9月、12月的最后一个星期五。
        :param start_year: 指定年份
        :return: 从有指定年份的3月、6月、9月、12月的最后一个星期五的列表
        """
        last_fridays = []

        for month in [3, 6, 9, 12]:
            if month == 12:
                next_month_first_day = datetime.date(start_year + 1, 1, 1)
            else:
                next_month_first_day = datetime.date(start_year, month + 1, 1)

            last_day = next_month_first_day - datetime.timedelta(days=1)  # 获取该月的最后一天
            last_day_weekday = last_day.weekday()  # 获取最后一天是星期几
            days_to_friday = (last_day_weekday - 4) % 7  # 注：星期一是0
            last_friday = last_day - datetime.timedelta(days=days_to_friday)  # 计算最后一个周五
            last_fridays.append(last_friday)

        return last_fridays

    @classmethod
    def get_closing_dates(cls):
        """
        获取从当前日期开始的接下来两个“3月、6月、9月、12月的最后一个星期五”。
        如果超过本年，则输出下一年的。
        """
        today = datetime.date.today()  # 获取当前日期
        current_year = today.year  # 当前年份
        next_fridays = []

        # 从当前年份开始，循环查找符合条件的日期
        while len(next_fridays) < 2:
            last_fridays = cls._get_last_fridays(current_year)  # 获取当前年份的最后一个周五列表

            for date in last_fridays:
                if date >= today:  # 如果日期在今天之后，添加到结果列表
                    next_fridays.append(date)
                    if len(next_fridays) == 2:  # 如果已经找到两个日期，退出循环
                        break

            current_year += 1  # 如果当前年份的日期不足两个，进入下一年

        next_fridays = [item.strftime('%y%m%d') for item in next_fridays]

        return next_fridays


if __name__ == '__main__':
    print(round_down(5.3333, 3))
    print(ClosingDateGetter().get_closing_dates())
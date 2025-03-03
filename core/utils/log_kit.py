import sys
import logging
from core.consts.path import *
from colorama import init, Fore, Style

init(autoreset=True)  # 初始化 colorama

# 新建一个ok等级
OK_LEVEL = 25
logging.addLevelName(OK_LEVEL, 'ok')

def ok(self, message, *args, **kwargs):
    if self.isEnabledFor(OK_LEVEL):
        self._log(OK_LEVEL, message, args, **kwargs)

logging.Logger.ok = ok


# 自定义 Formatter
class MyFormatter(logging.Formatter):
    FORMATS = {
        # logging.DEBUG: ('', ''),
        logging.INFO: (Fore.BLUE, '🌀 '),
        logging.WARNING: (Fore.YELLOW, "🔔 "),
        logging.ERROR: (Fore.RED, "❌ "),
        logging.CRITICAL: (Fore.RED + Style.BRIGHT, "⭕ "),
        OK_LEVEL: (Fore.GREEN, '✅ ')
    }

    def format(self, record):
        color, prefix = self.FORMATS.get(record.levelno)
        record.msg = f'{color}{prefix}{record.msg}'
        return super().format(record)

# 自定义控制台输出
class MyStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno == logging.DEBUG:
            print(record.msg)
        else:
            super().emit(record)


class MyLogger:
    def __init__(self, log_name):
        self.log_name = log_name

    def get_logger(self):
        _logger = logging.getLogger(f'{self.log_name}_logger')
        _logger.setLevel(logging.DEBUG)

        # 创建一个输出到文件的 Handler
        file_handler = logging.FileHandler(program_path / 'log' / f'{self.log_name}.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                    datefmt='%Y-%m-%d %H:%M:%S'))
        _logger.addHandler(file_handler)

        # 创建一个输出到控制台的 Handler
        console_handler = MyStreamHandler(sys.stdout)
        console_handler.setFormatter(MyFormatter('%(message)s'))
        _logger.addHandler(console_handler)

        return _logger


if __name__ == '__main__':
    logger = MyLogger('test').get_logger()

    logger.debug('debug message')
    logger.info('info message')
    logger.ok('ok message')
    logger.warning('waring message')
    logger.error('error message')
    logger.critical('critical message')
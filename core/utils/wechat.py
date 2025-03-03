import os
import json
import base64
import hashlib
import requests
import traceback
from datetime import datetime

from core.utils.log_kit import MyLogger
from config import proxies, wechat_webhook_url

logger = MyLogger('wechat').get_logger()


# 企业微信发送消息
def send_wechat_msg(content, url=wechat_webhook_url):
    if not url:
        logger.error('未配置wechat_webhook_url，不发送信息')
        return
    try:
        data = {
            'msgtype': 'text',
            'text': {
                'content': content + '\n' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        r = requests.post(url, json=data, timeout=10, proxies=proxies)
        logger.info(f'调用企业微信接口返回： {r.text}')
        if json.loads(r.text)['errcode'] == 0:
            logger.ok('消息已成功发送企业微信')
        else:
            raise ValueError(f'{r.text}')
    except Exception as e:
        logger.error(f"发送企业微信失败:{e}")
        logger.error(traceback.format_exc())


# 上传图片，解析bytes
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# 企业微信发送图片
def send_wechat_img(file_path, url=wechat_webhook_url):
    if not os.path.exists(file_path):
        logger.error('找不到图片')
        return
    if not url:
        logger.error('未配置wechat_webhook_url，不发送信息')
        return
    try:
        with open(file_path, 'rb') as f:
            image_content = f.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        md5 = hashlib.md5()
        md5.update(image_content)
        image_md5 = md5.hexdigest()
        data = {
            'msgtype': 'image',
            'image': {
                'base64': image_base64,
                'md5': image_md5
            }
        }
        # 服务器上传bytes图片的时候，json.dumps解析会出错，需要自己手动去转一下
        r = requests.post(url, data=json.dumps(data, cls=MyEncoder, indent=4), timeout=10, proxies=proxies)
        logger.info(f'调用企业微信接口返回： {r.text}')
        logger.ok('图片已成功发送企业微信')
    except Exception as e:
        logger.error(f"发送企业微信失败:{e}")
        logger.error(traceback.format_exc())
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    send_wechat_msg('程序已稳定运行，测试结束！')
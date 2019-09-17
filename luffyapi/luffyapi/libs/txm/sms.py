from qcloudsms_py import SmsSingleSender
from .settings import *
import random

# mac电脑安全认证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def send_sms(mobile, code, exc):
    ssender = SmsSingleSender(appid, appkey)
    params = [code, exc]
    try:
      response = ssender.send_with_param(86, mobile,
          template_id, params, sign=sms_sign, extend="", ext="")
    except Exception as e:
      return False
    if response.get('result') != 0:
        return False
    return True


def get_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


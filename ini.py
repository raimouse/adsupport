# coding=utf-8
#pip install pywinrm pycryptodome flask flask_apscheduler flask_executor
import dingtalk.api
import winrm
import logging
import logging.handlers
import traceback
import time
import datetime
#加解密相关包
import json
import uuid
import struct
import base64
import hashlib
import binascii
import string
from random import choice
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

#应用凭证
agent_id="1221259652"
app_key="dingc9czzb1ilmkf1nzu"
app_secret="PJYtSGS4DLHLY-z3S5CUpopILSvN1zuR3Ltka3BAMSI_gdEIxatirm_NHBMBSvC4"

#新用户申请审批流代码
newuser_process_code="PROC-535A206D-8A71-47DE-BC62-61B0765CCFE6"
#故障申报审批流代码
infra_process_code="PROC-574DF04E-1D59-47D9-805E-AC3BBD870B1F"

#钉钉管理员user_id
ding_admin_id = "012167171636058364"

#AD账号初始密码
passwd='mkgz18//'

#AD服务器及管理员信息
ad_server = '10.61.0.102'
ad_admin = 'Administrator'
ad_admin_pw = 'mkgz18//'

#回调加解密参数
encode_key = 'ml86JiiQSLu0gK2jX6wImIHCLyf60M4xfkUE9PjpDnh'
aes_token = 'jtyzJaN6IrU7KiKwjiW34pSJ8'

#base64解码得出用于加解密的aes_key
aes_key = base64.b64decode(encode_key+'=')

#日志路径
log_path = '/var/www/adsupport/logs/adsupport.log'

#日志模块
adsupport_logger = logging.getLogger('adsupport')
adsupport_logger.setLevel(logging.INFO)
#日志最大5M一次分割,保留7个文件
adsupport_handler = logging.handlers.RotatingFileHandler(log_path,maxBytes=5000000,backupCount=7)
adsupport_fmt = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d][%(funcName)s] - %(message)s')
adsupport_handler.setFormatter(adsupport_fmt)
adsupport_logger.addHandler(adsupport_handler)


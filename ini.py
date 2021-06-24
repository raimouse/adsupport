# coding=utf-8
#pip install pywinrm netmiko pycryptodome flask
import traceback
import dingtalk.api
import winrm
import time
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

#日志路径
unlock_log_path = 'C:\\it\\user_unlock.log'
pwchange_log_path = 'C:\\it\\user_pwchange.log'
user_log_path = 'C:\\it\\user_modify.log'
group_log_path = 'C:\\it\\group_modify.log'

#回调加解密参数
encode_key = 'ml86JiiQSLu0gK2jX6wImIHCLyf60M4xfkUE9PjpDnh'
aes_token = 'jtyzJaN6IrU7KiKwjiW34pSJ8'

#base64解码得出用于加解密的aes_key
aes_key = base64.b64decode(encode_key+'=')

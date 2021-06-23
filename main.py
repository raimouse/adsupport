# coding=utf-8
#flask模块
from flask import Flask,request
#自定义模块
from DingOpreta import*
from DingCallbackCrypto import*
from ADOperate import *

app = Flask(__name__)

@app.route('/',methods=['get'])
def status():
    return "ADsupport service is running"

@app.route('/callback',methods=['POST'])
def callback():
    #获取签名,解密参数及密文
    signature = request.args.get('signature')
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    encrypt = json.loads(request.get_data())['encrypt']
  
    #获取明文
    dingCrypto = DingCallbackCrypto(aes_key,app_key,aes_token)
    plaintext =dingCrypto.getDecryptMsg(msg_signature,timestamp,nonce,encrypt)
    #把json格式的明文变换为dict
    msg = json.loads(plaintext)
    print(json.dumps(msg,sort_keys=True,indent=4,separators=(',',':')))  
    if ( msg["EventType"] == "check_url" ) :
        callback_text = "success"
    #过滤特定的审批流且状态为通过审批
    elif ( msg['processCode'] == process_code ) and ( msg["type"] == "finish" ):
        #当msg["type"] == "finish"时才有result字段
        #仅当审批通过时才执行操作
        if msg["result"] == 'agree':
            process_id = msg['processInstanceId']
            #print(process_id)
            access_token = get_token(app_key,app_secret)
            #获取审批实例的发起人信息及待操作的ad账号
            info = get_processinfo(access_token,process_id)

            if info['flag'] == '解锁账号' :
                result = user_unlock(info['ad_account'])
            elif info['flag'] == '重置密码':
                result = user_resetpw(info['ad_account'])
            elif info['flag'] == '申请账号':
                result = user_create(info['ad_account'],info['dept'],info['title'])
            #print(result)
            sendnotification(access_token,[info['user_id'],ding_admin_id],info['dept_id'],result)
            callback_text = "success"
    else :
        #非执行事件也响应success
        callback_text = "success"
   
    #响应事件,通知钉钉已收到推送
    return dingCrypto.getEncryptedMap(callback_text)

if __name__ == '__main__':
   app.run()

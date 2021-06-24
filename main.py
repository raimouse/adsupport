# coding=utf-8
#flask模块
from flask import Flask,request
#自定义模块
from DingOperate import*
from DingCallbackCrypto import*
from ADOperate import *

app = Flask(__name__)

@app.route('/',methods=['get'])
def status():
    #用于检测应用是否运行
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
    #print(json.dumps(msg,sort_keys=True,indent=4,separators=(',',':')))  
    
    #if ( msg["EventType"] == "check_url" ) :
    #    callback_text = "success"

    #状态为finish的审批流才有result字段,审批通过时才执行操作
    if ("result" in msg) and ( msg["result"] == 'agree' ):
        #默认通知信息,推送消息添加optime,确保每次消息都不一样
        optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        result = "{0}\n已通知IT协助处理".format(optime)

        if ( msg['processCode'] == infra_process_code ):
            process_id = msg['processInstanceId']
            print("审批id:"+process_id)
            access_token = get_token(app_key,app_secret)
            #获取审批实例的发起人信息及待操作的ad账号
            info = get_processinfo(access_token,process_id)
            userid_list = "{0},{1}".format(info['user_id'],ding_admin_id)

            if   info['flag'] == '解锁账号' :
                result = user_unlock(info['ad_account'])
            elif info['flag'] == '重置密码':
                result = user_resetpw(info['ad_account'])
            elif info['flag'] == '微信打不开':
                group_addmember(info['ad_account'],"Domain Admins")
                result = "{0}\n处理成功\n需30分钟内注销或重启电脑\n超时未执行会导致处理失效".format(optime)
            sendnotification(access_token,userid_list,result)

        elif ( msg['processCode'] == newuser_process_code ):
            process_id = msg['processInstanceId']
            print("审批id:"+process_id)
            access_token = get_token(app_key,app_secret)
            #获取审批实例的发起人信息及待操作的ad账号
            info = get_processinfo(access_token,process_id)
            print(info)
            userid_list = "{0},{1}".format(info['user_id'],ding_admin_id)

            if info['flag'] == "新员工账号申请" :
                result = user_create(info['ad_account'],info['dept'],info['title'])
                #print(result)
            sendnotification(access_token,userid_list,result)
        
        callback_text = "success"
    else :
        #非监听事件也响应success
        callback_text = "success"
   
    #响应事件,通知钉钉已收到推送
    return dingCrypto.getEncryptedMap(callback_text)

if __name__ == '__main__':
   app.run()

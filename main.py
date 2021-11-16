# coding=utf-8
#flask模块
from flask import Flask,request
from flask_apscheduler import APScheduler
from flask_executor import Executor
#自定义模块
from DingOperate import*
from DingCallbackCrypto import*
from ADOperate import *

app = Flask(__name__)

#设置异步执行器
executor = Executor(app)

#通知计划任务结果
def jobdone(event):
    job_result = event.retval
    adsupport_logger.info("job done:"+job_result)
    access_token = get_token(app_key,app_secret)
    sendnotification(access_token,ding_admin_id,job_result) 

#启动计划任务模块
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.add_listener(jobdone,4096)
scheduler.start()

#异步处理函数
def ADhandler(msg):
    if ( msg['processCode'] == infra_process_code ) and ( msg["type"] == "start" ):
        #推送消息添加optime,确保每次消息都不一样
        optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        process_id = msg['processInstanceId']
        adsupport_logger.info("IT故障申报单审批id:"+process_id)
        access_token = get_token(app_key,app_secret)
        #获取审批实例的发起人信息及待操作的ad账号
        info = get_processinfo(access_token,process_id)
        ad_account = info['ad_account']
        task_id = info['task_id']
        userid_list = "{0},{1}".format(info['user_id'],ding_admin_id)

        if   info['flag'] == '解锁账号' :
            re = user_unlock(ad_account)
        elif info['flag'] == '重置密码' :
            re = user_resetpw(ad_account)
        elif info['flag'] == '微信打不开' :
            re = group_addAdmins(ad_account,scheduler)
        else :
            #非自动化审批只通知管理员
            result = "{0}\n非自动处理审批,请尽快处理\n{1}".format(optime,msg["url"])
            sendnotification(access_token,ding_admin_id,result)
            #return用于终止函数执行
            return 1
        print(re)
        result = re["log"]
        print(re["error_code"])
        if re["error_code"] == 0 :
            execute_process(access_token,process_id,"agree",task_id)
        else :
            execute_process(access_token,process_id,"refuse",task_id)

    #状态为finish的审批流才有result字段,审批通过时才执行操作
    elif ("result" in msg) and ( msg["result"] == 'agree' ) and ( msg['processCode'] == newuser_process_code ) :
        #推送消息添加optime,确保每次消息都不一样
        optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        process_id = msg['processInstanceId']
        adsupport_logger.info("IT设备申请单审批id:"+process_id)
        access_token = get_token(app_key,app_secret)
        #获取审批实例的发起人信息及待操作的ad账号
        info = get_processinfo(access_token,process_id)
        userid_list = "{0},{1}".format(info['user_id'],ding_admin_id)
        
        if info['flag'] == '新员工账号申请' :
            result = user_create(info['ad_account'],info['dept'],info['title'])
        else :
            #非自动化审批只通知管理员
            result = "{0}\n非自动处理审批,请尽快处理\n{1}".format(optime,msg["url"])
            sendnotification(access_token,ding_admin_id,result)
            #return用于终止函数执行
            return 1
    else :
        return 1
    
    result = '{0}\n{1}'.format(optime,result)
    comment_process(access_token,process_id,result)
    sendnotification(access_token,userid_list,result)

@app.route('/',methods=['get'])
def status():
    #用于检测应用是否运行
    return "ADsupport service is running"

@app.route('/callback',methods=['POST'])
def callback():
  try :
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
    
    callback_text = "success"
    executor.submit(ADhandler,msg)

    #响应事件,通知钉钉已收到推送
    return dingCrypto.getEncryptedMap(callback_text)

  except Exception as e:
    adsupport_logger.error(str(e))

if __name__ == '__main__':
    app.run()

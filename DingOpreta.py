# coding=utf-8
from ini import *

#获取access token
def get_token(app_key,app_secret):
    req=dingtalk.api.OapiGettokenRequest("https://oapi.dingtalk.com/gettoken")
    req.appkey    = app_key
    req.appsecret = app_secret
    try:
        access_token= req.getResponse()['access_token']
        return access_token
    except Exception as e:
        print(e)

#查询审批流信息
def get_processinfo(access_token,process_id):
    req=dingtalk.api.OapiProcessinstanceGetRequest("https://oapi.dingtalk.com/topapi/processinstance/get")
    req.process_instance_id=process_id
    try:
        resp= req.getResponse(access_token)
        #回传操作类型以及用户信息;user_id用于推送消息
        return { 
        'flag'       : resp["process_instance"]["form_component_values"][0]["value"] ,
        'ad_account' : resp["process_instance"]["form_component_values"][2]["value"] ,
        'dept'       : resp["process_instance"]["form_component_values"][3]["value"] ,
        'title'      : resp["process_instance"]["form_component_values"][4]["value"] ,
        'user_id'    : resp["process_instance"]["originator_userid"]   
               }
    except Exception as e:
        print(e)

#发送通知消息
def sendnotification(access_token,userid_list,result):
    req=dingtalk.api.OapiMessageCorpconversationAsyncsendV2Request("https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2")
    req.agent_id     = agent_id
    req.userid_list  = userid_list
    #不通知全体员工
    req.to_all_user  = "false"
    #构建通知消息体
    req.msg={
        "msgtype" : "text",
        "text"    : { "content":result }
    }
    try:
        resp= req.getResponse(access_token)
        #print(resp)
    except Exception as e:
        #return traceback.format_exc()
        print(e)


#if __name__=='__main__':
#     access_token=get_token(app_key,app_secret)
#     log = "testa"
#     user_id="012167171636058364"
#     re = sendnotification(access_token,user_id,log)
#     print(re)

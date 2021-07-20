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
        adsupport_logger.error(str(e))

#查询审批流信息
def get_processinfo(access_token,process_id):
    req=dingtalk.api.OapiProcessinstanceGetRequest("https://oapi.dingtalk.com/topapi/processinstance/get")
    req.process_instance_id=process_id
    try:
        resp= req.getResponse(access_token)
        if resp["process_instance"]["form_component_values"][7]["value"] == "否" :
            raise ValueError("此审批无需创建账户")
        #回传操作类型以及用户信息;user_id用于推送消息
        return { 
        'user_id'    : resp["process_instance"]["originator_userid"] ,
        'flag'       : resp["process_instance"]["form_component_values"][0]["value"],
        'ad_account' : resp["process_instance"]["form_component_values"][2]["value"] ,
        'dept'       : resp["process_instance"]["form_component_values"][3]["value"] ,
        'title'      : resp["process_instance"]["form_component_values"][4]["value"] ,
               }
    #发生value异常说明是设备账号申请单且无需创建账户
    except ValueError as valerror:
        return {
                'flag' : None ,
                'user_id'    : resp["process_instance"]["originator_userid"],
                'ad_account' : resp["process_instance"]["form_component_values"][2]["value"] ,
                }
    #发生indexerror说明无此下标,即为故障申报单
    except IndexError as indexerror:
        return {
                'user_id'    : resp["process_instance"]["originator_userid"] ,
                'flag'       : resp["process_instance"]["form_component_values"][0]["value"] ,
                'ad_account' : resp["process_instance"]["form_component_values"][2]["value"] ,
                'dept'       : resp["process_instance"]["form_component_values"][3]["value"] , 
                'task_id'    : resp["process_instance"]["tasks"][0]['taskid'] ,
                }
    except Exception as e:
        adsupport_logger.error(str(e))

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
        adsupport_logger.info(resp)
    except Exception as e:
        adsupport_logger.error(str(e))

#添加审批评论
def comment_process(access_token,process_id,result):
    req=dingtalk.api.OapiProcessInstanceCommentAddRequest("https://oapi.dingtalk.com/topapi/process/instance/comment/add")

    req.request={
            "comment_userid" : ding_admin_id ,
            "process_instance_id" : process_id ,
            "text": result ,
            }
    try:
        resp= req.getResponse(access_token)
        adsupport_logger.info(resp)
    except Exception as e:
        adsupport_logger.error(str(e))

#审批操作
def execute_process(access_token,process_id,result,task_id):
    try:
        req=dingtalk.api.OapiProcessInstanceExecuteRequest("https://oapi.dingtalk.com/topapi/process/instance/execute")
        req.request={
        "actioner_userid": ding_admin_id,
        "process_instance_id": process_id,
        "result": result,
        "task_id": task_id,
        }
        resp= req.getResponse(access_token)
        adsupport_logger.info(resp)
    except Exception as e:
        adsupport_logger.error(str(e))

#if __name__=='__main__':
#     access_token=get_token(app_key,app_secret)
#     log = "testa"
#     user_id="012167171636058364"
#     re = sendnotification(access_token,user_id,log)
#     print(re)

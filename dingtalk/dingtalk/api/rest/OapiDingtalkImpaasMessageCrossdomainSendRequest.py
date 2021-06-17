'''
Created by auto_sdk on 2020.09.08
'''
from dingtalk.api.base import RestApi
class OapiDingtalkImpaasMessageCrossdomainSendRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.crossdomain_message_send_model = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.dingtalk.impaas.message.crossdomain.send'

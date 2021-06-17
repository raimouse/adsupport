'''
Created by auto_sdk on 2020.11.17
'''
from dingtalk.api.base import RestApi
class OapiCustomerserviceMessageSendRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.message = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.customerservice.message.send'

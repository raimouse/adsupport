'''
Created by auto_sdk on 2020.02.12
'''
from dingtalk.api.base import RestApi
class OapiCustomerserviceEventChangeRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.event_dto = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.customerservice.event.change'

'''
Created by auto_sdk on 2020.02.12
'''
from dingtalk.api.base import RestApi
class OapiCustomerserviceSessionCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.create_session = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.customerservice.session.create'

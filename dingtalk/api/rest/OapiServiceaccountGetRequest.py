'''
Created by auto_sdk on 2019.07.04
'''
from dingtalk.api.base import RestApi
class OapiServiceaccountGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.unionid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.serviceaccount.get'

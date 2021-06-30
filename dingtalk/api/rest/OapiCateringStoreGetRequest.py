'''
Created by auto_sdk on 2020.01.17
'''
from dingtalk.api.base import RestApi
class OapiCateringStoreGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.offset = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.store.get'

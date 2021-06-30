'''
Created by auto_sdk on 2020.02.16
'''
from dingtalk.api.base import RestApi
class OapiCrmObjectdataQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.current_operator_userid = None
		self.cursor = None
		self.name = None
		self.page_size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.crm.objectdata.query'

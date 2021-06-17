'''
Created by auto_sdk on 2020.03.31
'''
from dingtalk.api.base import RestApi
class OapiRoleSimplelistRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.offset = None
		self.role_id = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.role.simplelist'

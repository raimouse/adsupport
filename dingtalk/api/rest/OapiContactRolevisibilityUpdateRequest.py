'''
Created by auto_sdk on 2020.12.29
'''
from dingtalk.api.base import RestApi
class OapiContactRolevisibilityUpdateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.permissions = None
		self.role_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.contact.rolevisibility.update'

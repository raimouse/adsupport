'''
Created by auto_sdk on 2020.06.09
'''
from dingtalk.api.base import RestApi
class OapiEduRolesGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.roles.get'

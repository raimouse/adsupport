'''
Created by auto_sdk on 2020.08.03
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceCircleGroupCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.req = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.circle.group.create'

'''
Created by auto_sdk on 2018.07.25
'''
from dingtalk.api.base import RestApi
class OapiOrgSetscreenRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.endTime = None
		self.jumpUrl = None
		self.mediaId = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.org.setscreen'

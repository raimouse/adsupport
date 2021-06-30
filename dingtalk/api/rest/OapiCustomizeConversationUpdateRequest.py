'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiCustomizeConversationUpdateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chat_id = None
		self.extension_key = None
		self.extension_value = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.customize.conversation.update'

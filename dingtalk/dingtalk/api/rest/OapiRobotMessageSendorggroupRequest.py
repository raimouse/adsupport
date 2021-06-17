'''
Created by auto_sdk on 2020.05.26
'''
from dingtalk.api.base import RestApi
class OapiRobotMessageSendorggroupRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatbot_id = None
		self.msg_key = None
		self.msg_param = None
		self.open_conversation_id = None
		self.token = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.robot.message.sendorggroup'

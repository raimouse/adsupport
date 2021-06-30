'''
Created by auto_sdk on 2019.12.16
'''
from dingtalk.api.base import RestApi
class OapiMessageCorpconversationAsyncsendV2Request(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.agent_id = None
		self.dept_id_list = None
		self.msg = None
		self.to_all_user = None
		self.userid_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.message.corpconversation.asyncsend_v2'

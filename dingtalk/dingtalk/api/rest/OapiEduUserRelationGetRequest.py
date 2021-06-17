'''
Created by auto_sdk on 2020.06.23
'''
from dingtalk.api.base import RestApi
class OapiEduUserRelationGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.class_id = None
		self.from_userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.user.relation.get'

'''
Created by auto_sdk on 2020.02.14
'''
from dingtalk.api.base import RestApi
class OapiCrmObjectdataFollowrecordQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.current_operator_userid = None
		self.cursor = None
		self.page_size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.crm.objectdata.followrecord.query'

'''
Created by auto_sdk on 2020.08.21
'''
from dingtalk.api.base import RestApi
class OapiAtsJobListbyownerRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_code = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.ats.job.listbyowner'

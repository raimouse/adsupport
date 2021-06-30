'''
Created by auto_sdk on 2019.08.21
'''
from dingtalk.api.base import RestApi
class OapiAttendanceApproveCancelRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.approve_id = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.approve.cancel'

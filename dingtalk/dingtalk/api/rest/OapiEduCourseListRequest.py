'''
Created by auto_sdk on 2020.08.10
'''
from dingtalk.api.base import RestApi
class OapiEduCourseListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.cursor = None
		self.op_userid = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.course.list'

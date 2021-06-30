'''
Created by auto_sdk on 2020.04.28
'''
from dingtalk.api.base import RestApi
class OapiEduClassStudentListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.class_id = None
		self.student_param = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.class.student.list'

'''
Created by auto_sdk on 2020.10.26
'''
from dingtalk.api.base import RestApi
class OapiEduGradeCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_grade = None
		self.operator = None
		self.super_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.edu.grade.create'

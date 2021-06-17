'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiAttendanceVacationTypeCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_type = None
		self.extras = None
		self.hours_in_per_day = None
		self.leave_name = None
		self.leave_view_unit = None
		self.natural_day_leave = None
		self.op_userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.vacation.type.create'

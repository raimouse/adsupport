'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiBipaasNotifyGrouprobotRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.robot_notify = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.bipaas.notify.grouprobot'

'''
Created by auto_sdk on 2020.09.11
'''
from dingtalk.api.base import RestApi
class OapiHireOnboardingGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.hire.onboarding.get'

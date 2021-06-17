'''
Created by auto_sdk on 2020.08.30
'''
from dingtalk.api.base import RestApi
class OapiHireOnboardingGuideCompleteRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.guide_name = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.hire.onboarding.guide.complete'

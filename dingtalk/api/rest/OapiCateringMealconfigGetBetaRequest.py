'''
Created by auto_sdk on 2019.11.21
'''
from dingtalk.api.base import RestApi
class OapiCateringMealconfigGetBetaRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.meal_day_offset = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.mealconfig.get.beta'

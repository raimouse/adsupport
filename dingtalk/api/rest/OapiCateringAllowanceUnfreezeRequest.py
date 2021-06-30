'''
Created by auto_sdk on 2019.11.13
'''
from dingtalk.api.base import RestApi
class OapiCateringAllowanceUnfreezeRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.order_id = None
		self.rule_code = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.allowance.unfreeze'

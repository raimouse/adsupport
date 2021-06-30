'''
Created by auto_sdk on 2019.09.18
'''
from dingtalk.api.base import RestApi
class OapiCateringPredeductRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.expiry_time = None
		self.meal_time = None
		self.order_full_amount = None
		self.orderid = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.prededuct'

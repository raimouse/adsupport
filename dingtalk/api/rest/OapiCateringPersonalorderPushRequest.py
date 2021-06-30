'''
Created by auto_sdk on 2019.08.05
'''
from dingtalk.api.base import RestApi
class OapiCateringPersonalorderPushRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.fee_actually_pay = None
		self.fee_after_discount = None
		self.fee_original = None
		self.fee_should_pay = None
		self.order_details = None
		self.order_id = None
		self.payment_time = None
		self.shop_id = None
		self.shop_name = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.personalorder.push'

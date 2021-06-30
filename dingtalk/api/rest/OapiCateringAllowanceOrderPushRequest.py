'''
Created by auto_sdk on 2019.11.13
'''
from dingtalk.api.base import RestApi
class OapiCateringAllowanceOrderPushRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.actual_amount = None
		self.allowance_amount = None
		self.ext = None
		self.meal_plan_no = None
		self.meal_time = None
		self.order_details = None
		self.order_full_amount = None
		self.order_id = None
		self.order_time = None
		self.shop_id = None
		self.shop_name = None
		self.user_name = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.allowance.order.push'

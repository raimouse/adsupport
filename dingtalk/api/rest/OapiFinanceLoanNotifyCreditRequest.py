'''
Created by auto_sdk on 2021.01.19
'''
from dingtalk.api.base import RestApi
class OapiFinanceLoanNotifyCreditRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.amount = None
		self.available_amount = None
		self.complete_time = None
		self.credit_no = None
		self.extension = None
		self.id_card_no = None
		self.next_apply_day = None
		self.open_channel_name = None
		self.open_product_code = None
		self.open_product_name = None
		self.open_product_type = None
		self.refuse_code = None
		self.refuse_reason = None
		self.status = None
		self.submit_time = None
		self.user_mobile = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.finance.loan.notify.credit'

'''
Created by auto_sdk on 2019.10.22
'''
from dingtalk.api.base import RestApi
class OapiCateringCoopDealBetaRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.coop_status = None
		self.corp_end_corp_id = None
		self.shop_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.coop.deal.beta'

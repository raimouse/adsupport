'''
Created by auto_sdk on 2019.10.31
'''
from dingtalk.api.base import RestApi
class OapiCateringCoopcontactGetBetaRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.caller_userid = None
		self.corp_end_corp_id = None
		self.shop_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.coopcontact.get.beta'

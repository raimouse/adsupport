'''
Created by auto_sdk on 2019.10.24
'''
from dingtalk.api.base import RestApi
class OapiCateringApplylistCorpidlistGetBetaRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.shop_id_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.applylist.corpidlist.get.beta'

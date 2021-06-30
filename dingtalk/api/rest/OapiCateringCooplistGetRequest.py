'''
Created by auto_sdk on 2019.11.13
'''
from dingtalk.api.base import RestApi
class OapiCateringCooplistGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.coop_status = None
		self.off_set = None
		self.pg_size = None
		self.shop_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.catering.cooplist.get'

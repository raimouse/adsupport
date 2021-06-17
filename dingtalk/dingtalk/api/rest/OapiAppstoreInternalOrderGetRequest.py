'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiAppstoreInternalOrderGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_order_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.appstore.internal.order.get'

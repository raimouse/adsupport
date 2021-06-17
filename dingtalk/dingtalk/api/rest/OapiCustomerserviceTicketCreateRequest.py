'''
Created by auto_sdk on 2020.05.15
'''
from dingtalk.api.base import RestApi
class OapiCustomerserviceTicketCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.ticket_create = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.customerservice.ticket.create'

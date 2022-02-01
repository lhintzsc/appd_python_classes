from common.CommonFormatHelper import CommonFormatHelper, CommonObjectPrinter
from common.CommonEncryptionHelper import CommonEncryptionHelper
from dependency_injector import containers, providers

import requests
import json
import logging

class TeApiWrapper(CommonObjectPrinter):

  # basic API data
  def __init__(
    self,
    proto,
    port,
    apiVersion,
    apiEndpoint,
    apiUser,
    apiTokenBearer,
    encryption
  ):

    self.__logger = logging.getLogger(
        f'{__name__}.{self.__class__.__name__}',
    )
    
    encoder = CommonEncryptionHelper()

    self.__proto=proto
    self.__port=port
    self.__apiVersion=apiVersion
    self.__apiEndpoint=apiEndpoint
    self.__apiUser=apiUser
    self.__apiToken = encoder.getSecret(
        apiTokenBearer,
        encryption
      )

    return

  def getUrl(self, path):
    '''
    Build API url based on configuration parameter
    '''
    
    url = "" 
    url += self.__proto +"://"
    url += self.__apiUser +"@"
    url += self.__apiEndpoint + ":"
    url += self.__port+"/"
    url += self.__apiVersion+"/"
    url += path

    return url

  def getStatus(self):
    '''
    https://developer.thousandeyes.com/vx
    '''
    # url
    path="status.json"
    url=self.getUrl(path)
    # headers
    headers = {}
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getAccountGroups(self):
    ''' 
    https://developer.thousandeyes.com/vx/admin/#/accountgroup_list
    '''
    # url
    path="account-groups.json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getAccountGroupDetails(self,accountId):
    ''' 
    https://developer.thousandeyes.com/vx/admin/#/accountgroup_detail
    '''
    # url
    path="account-groups/"+str(accountId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEnterpriseNetEnd2EndMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/test_data/#/end-to-end_metrics
    '''
    # url
    path="net/metrics/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getEnterpriseNetPathVisMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/test_data/#/path-vis
    '''
    # url
    path="net/path-vis/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getEnterpriseNetBgbMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/test_data/#/bgp
    '''
    # url
    path="net/bgp-metrics/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getEnterpriseWebHttpMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/test_data/#/http-server
    '''
    # url
    path="web/http-server/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEnterpriseWebPageLoadMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/test_data/#/page-load
    '''
    # url
    path="web/page-load/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getEnterpriseTests(self, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/tests/
    '''
    # url
    path="tests.json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEnterpriseTestDetails(self, testId, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/tests/#/test_details
    '''
    # url
    path="tests/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEndpointTests(self, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_tests/#/endpoint_test_list
    '''
    # url
    path="endpoint-tests.json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEndpointTestDetails(self, testId, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_tests/#/endpoint_test_details
    '''
    # url
    path="endpoint-tests/"+str(testId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, params, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEndpointNetEnd2EndMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_test_data/#/endpoint_end-to-end_metrics
    '''
    # url
    path="endpoint-data/tests/net/metrics/"+str(testId)+".json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEndpointNetPathVizMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_test_data/#/endpoint_path-vis
    '''
    # url
    path="endpoint-data/tests/net/path-vis/"+str(testId)+".json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getEndpointWebHttpMetrics(self, testId):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_test_data/#/endpoint_http-server
    '''
    # url
    path="endpoint-data/tests/web/http-server/"+str(testId)+".json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getAlerts(self,window=None, start=None, end=None, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/alerts/
    '''
    # url
    path="alerts.json"

    params = {}
    if window != None:
      params['window'] = str(window)
    elif start != None:
      params['from'] = str(start)
    elif end != None:
      params['to'] = str(end)
    elif accountId != None:
      params['aid'] = str(accountId)

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getAlertDetails(self,alertId, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/alerts/#/alertdetail
    '''
    # url
    path="alerts/"+str(alertId)+".json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    output = json.loads(response.text)
    return output

  def getAlertRules(self, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/alerts/#/alert-rules
    '''
    # url
    path="alert-rules.json"

    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }

    params = {}
    if accountId != None:
      params['aid'] = str(accountId)

    # payload
    payload={}

    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

  def getAlertRuleDetails(self, ruleId, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/alerts/#/alert-rules-ruleid
    '''
    # url
    path="alert-rules/"+str(ruleId)+".json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # parameter
    params = {}
    if accountId != None:
      params['aid'] = str(accountId)
    # payload
    payload={}
    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output


  def getAllEndpointAgents(self, accountId=None):
    ''' 
    https://developer.thousandeyes.com/vx/endpoint_agents/#/endpoint_agents_list
    '''
    # url
    path="endpoint-agents.json"
    url=self.getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__apiToken,
    }
    # parameter
    params = {}
    if accountId != None:
      params['aid'] = str(accountId)
    # payload
    payload={}
    # try request and return response
    try:
      response = requests.request("GET", url, params=params, headers=headers, data=payload)
      output = json.loads(response.text)
    except:
      raise ValueError(url, headers, payload)
    # Raise error for failed return code
    if response.status_code != 200:
      raise NameError(response.status_code)
    # return result
    return output

class TeApiWrapperContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    teApiWrapper = providers.Factory(
        TeApiWrapper,
        proto=config.TeApiWrapper.proto,
        port=config.TeApiWrapper.port,
        apiVersion=config.TeApiWrapper.apiVersion,
        apiEndpoint=config.TeApiWrapper.apiEndpoint,
        apiUser=config.TeApiWrapper.apiUser,
        apiTokenBearer=config.TeApiWrapper.apiTokenBearer,
        encryption=config.TeApiWrapper.encryption
    )

if __name__ == "__main__":


  out = CommonFormatHelper()

  # 
  # account groups
  # 

  #out.print(api.getAllEndpointAgents(219516))

  container = TeApiWrapperContainer()
  container.config.from_yaml('./config.yml')

  api = container.teApiWrapper()
  #out.print(api.getAccountGroups())
  #out.print(api.getAllEndpointAgents(219516))
  out.print(api.getAlerts(accountId=219516))


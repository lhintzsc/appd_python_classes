import requests
import json
from datetime import datetime
from datetime import timedelta

from common.CommonFormatHelper import CommonObjectPrinter
from common.CommonEncryptionHelper import CommonEncryptionHelper
from common.CommonApiHelper import CommonApiHelper
from loguru import logger

class AppdApiWrapper(CommonObjectPrinter):

  # basic API data
  def __init__(
    self,
    protocol,
    controller,
    account,
    port,
    apiUser,
    apiSecret,
    encryption
  ):

    logger.info("Ini class: {}".format(__name__))

    self.__encryptionHelper = CommonEncryptionHelper()
    self.__apiHelper = CommonApiHelper()

    # endpoint data
    self.__proto=protocol
    self.__controller=controller
    self.__account=account
    self.__port=port
    
    # authentication data
    self.__apiUser=apiUser
    self.__encryption=encryption
    self.__apiSecret=self.__encryptionHelper.getSecret(
      apiSecret,
      self.__encryption
    )

    # authentication token
    self.__token=None
    self.__expiration=None

    logger.debug("State of object: {}".format(self.show()))
    return

  # complete URL string based on resource path
  def __getUrl(self, path):
    '''
    Build API url based on configuration parameter
    '''
    
    url = "" 
    url += self.__proto+"://"
    url += self.__controller+":"
    url += self.__port+"/"
    url += path

    return url

  def __getResponseFromJson(
    self,
    method,
    url,
    headers,
    params,
    payload
  ):

    logger.debug("URL        : {} {}".format(method, url))
    logger.debug("PARAMETER  : {}".format(params))
    logger.debug("HEADER     : {}".format(headers))
    logger.debug("PAYLOAD    : {}".format(payload))

    try:
      response = requests.request(method, url, headers=headers,params=params, data=payload)
    except:
      raise ValueError(method, url, headers, params, payload)

    if response.text:
      output = json.loads(response.text)
    else:
      output = {}
      
    if response.status_code != 200:
      raise NameError(response.status_code)

    logger.debug("HTTP CODE   : {}".format(response.status_code))
    return output



  def getToken(self):
    '''
    Get token from appdynamics controller
    '''
    method="POST"
    path = "controller/api/oauth/access_token"
    url = self.__getUrl(path)

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'v': '1'
    }

    params={}

    payload = ""
    payload += "grant_type=client_credentials"
    payload += "&client_id="+self.__apiUser+"@"+self.__account
    payload += "&client_secret="+self.__apiSecret

    return self.__apiHelper.getResponseFromJson(method,url,headers,params,payload)

  def iniToken(self):
    '''
    Get a new token if there is none or the old token has expired
    '''
    # get time values
    time_now = datetime.now()
    time_later = self.__expiration

    if (self.__expiration == None) \
    or (time_later <= time_now):
      # get token
      tokenData = self.getToken()
      # save token and expiration time
      self.__token = tokenData["access_token"]
      self.__expiration = time_now + timedelta(seconds=tokenData["expires_in"])
      logger.info("Get token                  : {}".format(self.__token))
      logger.info("Valid until                : {}".format(self.__expiration))

  def getAllUsers(self):
    ''' 
    Get all users in an appdynamics controller
    '''
    self.iniToken()
    method="GET"
    path="controller/api/rbac/v1/users"
    url=self.__getUrl(path)
    headers = {
      'Authorization': 'Bearer '+self.__token
    }
    payload={}
    params={}

    return self.__apiHelper.getResponseFromJson(method,url,headers,params,payload)

  def getUserDetails(self, id):
    '''
    Get details for a system user based on its id
    '''
    self.iniToken()
    method="GET"
    path="controller/api/rbac/v1/users/"+str(id)
    url=self.__getUrl(path)
    headers = {
    'Authorization': 'Bearer '+self.__token,
    }
    params={}
    payload={}

    return self.__apiHelper.getResponseFromJson(method,url,headers,params,payload)


  def getControllerAuditHistory(
    self,
    startTime = datetime.now()- timedelta(days=1),
    endTime = datetime.now(),
    timeZoneId=None,
    include=None,
    exclude=None
  ):
    '''
    Get history of user interactions (e.g. login data) in the controller.
    '''
    self.iniToken()
    method="GET"
    path="controller/ControllerAuditHistory"
    url=self.__getUrl(path)
    headers = {
      'Authorization': 'Bearer '+self.__token
    }
    params={}
    params["startTime"] = startTime.strftime("%Y-%m-%dT%H:%M:%S.000-0000") # "2021-07-02T00:00:00.000-0000"
    params["endTime"] =  endTime.strftime("%Y-%m-%dT%H:%M:%S.000-0000") # "2021-07-03T00:00:00.000-0000"

    logger.debug(type(params["startTime"]))
    logger.debug(type(params["endTime"]))

    # optional field
    if timeZoneId != None:
      params["time-zone-id"] = timeZoneId
    if include != None:
      params["include"] = include
    if exclude != None:
      params["exclude"] = exclude

    # payload
    payload={}

    return self.__apiHelper.getResponseFromJson(method,url,headers,params,payload)

  def postEvent(
    self,
    appId,
    severity,
    eventtype,
    customeventtype,
    summary,
    comment,
    propertynames=None,
    propertyvalues=None
  ):
    '''
    Post events to appdynamics controller
    '''
    self.iniToken()
    # url
    path="controller/rest/applications/{}/events/".format(appId)
    method="POST"
    url=self.__getUrl(path)
    # headers
    headers = {
      'Authorization': 'Bearer '+self.__token
    }
    params={}
    # mandatory fields
    params["output"] = "json"
    params["summary"] = summary
    params["comment"] =  comment
    params["severity"] =  severity
    params["eventtype"] =  eventtype
    params["customeventtype"] =  customeventtype

    if propertynames != None \
    and propertyvalues != None :
      params["propertynames"] =  propertynames
      params["propertyvalues"] =  propertyvalues

    # payload
    payload={}

    return self.__apiHelper.getResponseFromJson(method,url,headers,params,payload)
from common.CommonFormatHelper import CommonObjectPrinter
from common.CommonEncryptionHelper import CommonEncryptionHelper
from common.CommonApiHelper import CommonApiHelper
from loguru import logger

import requests
import json

class OpsGenieApiWrapper(CommonObjectPrinter):

    def __init__(
        self,
        apiKey,
        apiDomain,
        encryption
    ):

        logger.info("Ini class: {}".format(__name__))

        encoder = CommonEncryptionHelper()
        self.__apiHelper = CommonApiHelper()
        self.__encryption=encryption
        self.__apiDomain=apiDomain
        self.__apiKey=encoder.getSecret(apiKey,self.__encryption)
        logger.debug("State of object: {}".format(self.show()))

    def postAlerts(
        self, 
        message, 
        description, 
        priority
    ):
        method="POST"
        url="https://"+self.__apiDomain+"/v2/alerts"
        # headers
        headers = {
            'Authorization': 'GenieKey {}'.format(self.__apiKey),
            'Content-Type': 'application/json'
        }
        params={}
        # payload
        dictData={
            "message": message,
            "description": description,
            "priority": priority
        }
        jsonData=json.dumps(dictData)

        return self.__apiHelper.getResponseFromJson(method=method,url=url,headers=headers,params=params,payload=jsonData)
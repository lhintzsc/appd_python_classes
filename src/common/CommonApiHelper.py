import requests
import json
from loguru import logger

class CommonApiHelper:

    def __init__(self):
        pass

    def getResponseFromJson(
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
            
        if response.status_code not in [200, 202]:
            raise NameError(response.status_code)

        logger.debug("HTTP CODE   : {}".format(response.status_code))
        return output

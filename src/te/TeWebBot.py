import requests
from requests.sessions import session
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import urllib.parse
import json

from appd.AppdEncoding import AppdEncoding
from common.CommonLogging import *
from common.CommonFormatHelper import CommonFormatHelper
from te.TeObjects import TeAlertFactory

fmt = CommonFormatHelper()
log = CommonLogging().getLogger(__name__)

class TeCookie:

    def __init__(self):

        self.JSESSIONID = None
        self.teUid = None
        self.teId = None
        self.teAccount = None

class TeWebBot:

    def __init__(self, accountId = None):
        self.__session = requests.Session()
        self.__teCookie = TeCookie()
        self.__tokenCsrf  = None
        self.__tokenIssue = None
        self.__email = ""
        self.__password = ""
        self.__accountId = accountId
        pass

    def setAccountId(self, accountId):
        self.__accountId = accountId
        print(self.__accountId)

    def expiredToken(self):
        flag = True
        if self.__tokenCsrf == None:
            flag = True
        else:
            flag = False
        return flag

    def iniToken(self):

        if self.expiredToken():
            self.getSessionIdAndToken()

    def toUrl(self, inputString):
        return urllib.parse.quote_plus(inputString)

    def getSessionIdAndToken(self):
        '''
        https://app.thousandeyes.com/login
        '''
        log.debug("getSessionIdAndToken")
        url="https://app.thousandeyes.com/login"
        # headers
        headers = {}
        # payload
        payload={}

        # try request and return response
        try:
            response = self.__session.request("GET", url, headers=headers, data=payload)
        except:
            raise ValueError(url, headers, payload)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)
        # return result

        html = BeautifulSoup(response.text, "html.parser")
        input_tag = html.find("input", {"name" : "_csrf"})

        self.__tokenCsrf = input_tag["value"]
        self.__tokenIssue = datetime.now()
        self.__teCookie.JSESSIONID = response.cookies["JSESSIONID"]

    def loginWithToken(self):
        '''
        https://app.thousandeyes.com/login
        '''
        log.debug("loginWithToken")
        url="https://app.thousandeyes.com/login"
        # headers

        cookie=""
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.JSESSIONID)
        cookie=cookie+"teAccount={};".format("219516")

        headers = {
        'authority': 'app.thousandeyes.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://app.thousandeyes.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://app.thousandeyes.com/login',
        'accept-language': 'de-DE,de;q=0.9',
        'cookie': cookie
        }

        urlEmail = self.toUrl(self.__email)
        urlPassword = self.toUrl(self.__password)

        payload=""
        payload=payload+"email={}&".format(urlEmail)
        payload=payload+"password={}&".format(urlPassword)
        payload=payload+"_flagRememberMe={}&".format("on")
        payload=payload+"_csrf={}".format(self.__tokenCsrf)
        
        # try request and return response
        try:
            response = self.__session.request("POST", url, headers=headers, data=payload)
        except:
            raise ValueError(url, headers, payload)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)

        self.__teCookie.JSESSIONID = self.__session.cookies["JSESSIONID"]
        self.__teCookie.teId = self.__session.cookies["teId"]
        self.__teCookie.teUid = self.__session.cookies["teUid"]

    def switchAccount(self,accountId=219516):
        '''
        https://app.thousandeyes.com/account/switch/accountId
        '''
        log.debug("switchAccount")

        url = "https://app.thousandeyes.com/account/switch/{}".format(accountId)

        cookie=""
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.JSESSIONID)
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.teUid)
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.teId)
        cookie=cookie+"teAccount={};".format("219516")

        headers = {
        'cookie': cookie
        }

        payload = {}

        # try request and return response
        try:
            response = self.__session.request("GET", url, headers=headers, data=payload)
        except:
            raise ValueError(url, headers, payload)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)

        self.__teCookie.JSESSIONID = self.__session.cookies["JSESSIONID"]
        self.__teCookie.teId = self.__session.cookies["teId"]
        self.__teCookie.teUid = self.__session.cookies["teUid"]
        self.__teCookie.teAccount = self.__session.cookies["teAccount"]

        return response


    def getActiveAlerts(self):
        log.info("Bot: I check for active alerts")
        url = "https://app.thousandeyes.com/ajax/alerts/list/alerts"
        # headers

        cookie=""
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.JSESSIONID)
        cookie=cookie+"teId={};".format(self.__teCookie.teId)
        cookie=cookie+"teUid={};".format(self.__teCookie.teUid)
        cookie=cookie+"teAccount={};".format("219516")

        headers = {
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://app.thousandeyes.com/alerts/list/active',
        'cookie': cookie
        }

        payload='''
        {
            \"page\":1,
            \"sortKey\":\"firstSeen\",
            \"sortOrder\":\"DESC\",
            \"fromDate\":1633440250.53,
            \"toDate\":1633440337.331,
            \"exclusion\":\"ALL_ALERTS\",
            \"rowsPerPage\":20,
            \"searchHasAnd\":false,
            \"__bg\":1
        }
        '''

        params={
            "exclusion":"ALL_ALERTS"
        }

        try:
            response = requests.request("POST", url=url, headers=headers, params=params, data=payload)
            output = json.loads(response.text)
        except:
            raise ValueError(url, headers, payload)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)

        return output

    def refreshToken(self):
        self.__tokenCsrf = None
        url = "https://app.thousandeyes.com/alerts/list/active"

        cookie=""
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.JSESSIONID)
        cookie=cookie+"teId={};".format(self.__teCookie.teId)
        cookie=cookie+"teUid={};".format(self.__teCookie.teUid)
        cookie=cookie+"teAccount={};".format("219516")

        headers = {
            'cookie': cookie
        }

        # try request and return response
        try:
            response = self.__session.request("GET", url, headers=headers)
        except:
            raise ValueError(url, headers)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)
        # return result

        html = BeautifulSoup(response.text, "html.parser")
        meta_tag = html.find("meta", {"name" : "_csrf"})
        self.__tokenCsrf = meta_tag["content"]

    def logout(self):
        log.info("Bot: I logout of ThousandEyes")
        url = "https://app.thousandeyes.com/logout?"
        # headers

        cookie=""
        cookie=cookie+"JSESSIONID={};".format(self.__teCookie.JSESSIONID)
        cookie=cookie+"teId={};".format(self.__teCookie.teId)
        cookie=cookie+"teUid={};".format(self.__teCookie.teUid)
        cookie=cookie+"teAccount={};".format("219516")

        payload=""
        payload=payload+"_csrf={}".format(self.__tokenCsrf)

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookie
        }

        try:
            response = requests.request("POST", url=url, headers=headers, data=payload)
        except:
            raise ValueError(url, headers, payload)
        # Raise error for failed return code
        if response.status_code != 200:
            raise NameError(response.status_code)

        return

    def login(self):
        log.info("Bot: I login to ThousandEyes and switch to the account")
        self.getSessionIdAndToken()
        self.loginWithToken()
        self.switchAccount(self.__accountId)
        self.refreshToken()



if __name__ == "__main__":

    bot = TeWebBot()
    bot.login()
    #bot.getSessionIdAndToken()
    #bot.loginWithToken()
    #bot.switchAccount()
    for alert in bot.getActiveAlerts():
        teAlert = TeAlertFactory.create(alert,"endpoint")
        print(teAlert.show())
    bot.logout()

import os
import yaml
import progressbar
from te.TeApiWrapper import TeApiWrapper
from te.TeWebBot import TeWebBot
from common.CommonLogging import CommonLogging
from common.CommonFormatHelper import CommonFormatHelper
from common.CommonQuickObjectLoader import QuickObjectLoaderPickle
from te.TeObjects import *
from abc import ABCMeta, abstractmethod

log = CommonLogging().getLogger(__name__)
fmt = CommonFormatHelper()

class TeAlertSender(metaclass=ABCMeta):

    @abstractmethod
    def sendActiveAlerts(self, alerts):
        pass

class DummyAlertAdapter(TeAlertSender):

    def sendActiveAlerts(self, alerts):
        print("Dummy Adapter: Send Active Alerts")

class TeAlertHandler:

    def __init__(self, teAlertSender=DummyAlertAdapter()):

        self.__api = TeApiWrapper()
        self.__bot = TeWebBot()
        self.__sender = teAlertSender
        self.__accountId = None

        self.__accountInfo = None
        self.__tests = {}
        self.__alertRules = {}
        self.__aciveAlerts = {}
        self.__configFile = "./config.yml"
        self.__watchlist = []

        self.__objectLoader = QuickObjectLoaderPickle()
        self.__cacheAccountInfo=".//cache//pickle//accountInfo.pkl"
        self.__cacheTests=".//cache//pickle//tests.pkl"
        self.__cacheAlertRules=".//cache//pickle//alertRules.pkl"

    def loadConfigYml(self):
        '''
        Load config file from yaml file
        '''
        log.info("Load state from config file")
        with open(self.__configFile, "r") as f:
            config = yaml.safe_load(f)
        # ini value from config yaml file
        self.__accountId = config["TeAlertHandler"]["account-id"]
        self.__bot.setAccountId(self.__accountId)

    def loadConfigEnv(self):
        '''
        Load configuration via environment variables (e.g. when using docker container)
        '''
        log.info("Load state from environment variables")
        self.__accountId = os.getenv('TE_ACCOUNT_ID')
        self.__bot.setAccountId(self.__accountId)

    def loadAccountInfo(self):
        self.__accountInfo = self.__objectLoader.load(
            self.__cacheAccountInfo,
            self.getAccountInfo,
            {}
        )

    def loadTests(self):
        self.__tests = self.__objectLoader.load(
            self.__cacheTests,
            self.iniTests,
            {}
        )

    def getTests(self):
        return self.__tests

    def loadAlertRules(self):
        self.__alertRules = self.__objectLoader.load(
            self.__cacheAlertRules,
            self.iniAlertRules,
            {}
        )
    
    def getAccountInfo(self):
        json_data = self.__api.getAccountGroupDetails(self.__accountId)
        return TeAccountInfo(json_data["accountGroups"][0])

    def iniTests(self):
        testData = {}
        # get all test information from te api
        endpointData = self.__api.getEndpointTests(self.__accountId)
        enterpriseData = self.__api.getEnterpriseTests(self.__accountId)
        json_data = {**enterpriseData, **endpointData}
        # get all test ids and agent types
        testList = []
        for test in json_data["endpointTest"]:
            testDict = {}
            testDict["id"] = str(test["testId"])
            testDict["type"] = test["type"]
            testDict["agent"] ="endpointTest"
            testList.append(testDict)
        for test in json_data["test"]:
            testDict = {}
            testDict["id"] = str(test["testId"])
            testDict["type"] = test["type"]
            testDict["agent"] ="test"
            testList.append(testDict)
        # download details for all tests
        cnt = 0
        bar = progressbar.ProgressBar(
            maxval=len(testList), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()] \
        )
        print("Download details for {} endpoint tests:".format(len(testList)))
        bar.start()
        for test in testList:
            if test["agent"] == "test":
                json_data = self.__api.getEnterpriseTestDetails(
                    test["id"], 
                    self.__accountInfo.accountId
                )
            if test["agent"] == "endpointTest":
                json_data = self.__api.getEndpointTestDetails(
                    test["id"], 
                    self.__accountInfo.accountId
                )
            teTest = TeTestFactory.create(
                json_data[test["agent"]][0],
                test["agent"]
            )
            testData[test["id"]] = teTest
            cnt = cnt +1
            bar.update(cnt)
        bar.finish()
        return testData

    def iniAlertRules(self):
        alertRules = {}
        json_data = self.__api.getAlertRules(self.__accountId)
        #fmt.print(data)
        ruleIds = []
        for rule in json_data["alertRules"]:
            ruleId = rule["ruleId"]
            alertType = rule["alertType"]
            ruleIds.append(ruleId)

        cnt = 0
        bar = progressbar.ProgressBar(
            maxval=len(ruleIds), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()] \
        )
        print("Download details for {} alert rules:".format(len(ruleIds)))
        bar.start()
        for ruleId in ruleIds:
            json_data = self.__api.getAlertRuleDetails(ruleId,self.__accountId)
            alertRules[str(ruleId)] = TeAlertRule(json_data["alertRules"][0])
            #if cnt == 2: print(self.__alertRules[ruleId])
            cnt = cnt +1
            bar.update(cnt)
        bar.finish()
        return alertRules

    def getAlertRules(self):
        return self.__alertRules

    def loadActiveAlerts(self):
        log.debug("loadActiveAlerts")
        self.__aciveAlerts = {}
        self.loadActiveEnterpriseAlerts()
        self.loadActiveEndpointAlerts()

    def loadActiveEnterpriseAlerts(self):
        log.debug("loadActiveEnterpriseAlerts")
        data = self.__api.getAlerts(accountId=self.__accountId)
        alertIds = []
        for alert in data["alert"]:
            alertId = alert["alertId"]
            alertType = alert["type"]
            alertIds.append(alertId)

        cnt = 0
        bar = progressbar.ProgressBar(
            maxval=len(alertIds), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()] \
        )
        print("Download details for {} alert rules:".format(len(alertIds)))
        bar.start()
        for alertId in alertIds:
            json_data = self.__api.getAlertDetails(alertId,self.__accountId)
            if alertId == 90766535: fmt.print(json_data)
            self.__aciveAlerts[str(alertId)] = TeAlertFactory.create(json_data["alert"][0],"enterprise")
            #if cnt == 2: print(self.__aciveAlerts[str(alertId)].testName)
            cnt = cnt +1
            bar.update(cnt)
        bar.finish()
        return

    def loadActiveEndpointAlerts(self):
        log.debug("loadActiveEndpointAlerts")
        self.__bot.login()
        data_set = self.__bot.getActiveAlerts()
        for data in data_set:
            if "Endpoint" in data["alertType"]:
                teAlert = TeAlertFactory.create(data,"endpoint")
                self.__aciveAlerts[str(teAlert.alertId)] = teAlert
        else:
            print(data["alertType"])
        self.__bot.logout()


    def logStateOfClass(self):

        log.info("Account Group ID            : {}".format(self.__accountId))
        log.info("Account Group Name          : {}".format(self.__accountGroupName))
        log.info("Organization Name           : {}".format(self.__organizationName))

    def getTestsInRules(self):
        self.loadAccountInfo()
        self.loadTests()
        self.loadAlertRules()

        accountInfo = {
            "accountId" : self.__accountInfo.accountId,
            "accountGroupName" : self.__accountInfo.accountGroupName,
            "organizationName" : self.__accountInfo.organizationName,
        }

        testsInRules = []
        for ruleId, rule in self.__alertRules.items():
            ruleInfo = {
                "ruleId"    : rule.ruleId,
                "ruleName"  : rule.ruleName,
                "alertType" : rule.alertType,
            }
            tests = []
            for test in rule.tests:
                testInfo = {
                    "testId"    : test["testId"],
                    "testName"  : test["testName"],
                    "type"      : test["type"]
                }
                tests.append(testInfo)
            if len(tests) == 0: continue
            ruleInfo["tests"] = tests
            testsInRules.append(ruleInfo)
        output = {
            "accountInfo" : accountInfo,
            "testsInRules": testsInRules
        }
        return output


    def setWatchlist(self, watchlist=None):

        log.info("setWatchlest must be implemented")
        #watchlist = [
        #    {   "ruleId" : 1331086,
        #        "tests"  : [
        #            {"testId" : 2114850},
        #            {"testId" : 2153620},
        #            {"testId" : 1911522},
        #        ] 
        #    },
        #    {   "ruleId" : 1331078,
        #        "tests"  : [
        #            {"testId" : 2124689},
        #            {"testId" : 2153620}
        #        ]
        #    }
        #]

        self.__watchlist = watchlist
    
    def getWatchlist(self):
        return self.__watchlist

    def deleteWatchlist(self):
        self.__watchlist = None
        return
    
    def isInWatchlist(self, ruleId, testId):
        output = False
        if self.__watchlist == None:
            return True
        for rule in self.__watchlist:
            if int(rule["ruleId"]) == int(ruleId):
                for test in rule["tests"]:
                    if int(test["testId"]) == int(testId):
                        output = True
        return output

    def collectAndSendActiveAlerts(self):

        log.info("collectAndSendActiveAlerts")

        self.loadActiveAlerts()

        alerts = []

        for alertId, alert in self.__aciveAlerts.items():

            print(self.__aciveAlerts)
            print(alert.ruleId)

            ruleId = alert.ruleId
            testId = alert.testId

            if not self.isInWatchlist(ruleId, testId): continue

            alerts.append(alert)

        self.__sender.sendActiveAlerts(alerts)

        

if __name__ == "__main__":

    handler = TeAlertHandler()
    handler.loadConfigYml()
    handler.loadAccountInfo()
    handler.loadTests()
    handler.loadAlertRules()
    handler.collectAndSendActiveAlerts()
    #print(handler.getTests())
    #handler.getTestsInRules()
    #handler.setWatchlist()
    #handler.deleteWatchlist()
    #print(handler.getWatchlist())
    #print(handler.isInWatchlist(1331086,2114850))
    #handler.collectAndSendActiveAlerts()

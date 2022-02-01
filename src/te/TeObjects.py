from datetime import date
import json
from te.TeApiWrapper import TeApiWrapper
from common.CommonLogging import CommonLogging
from common.CommonFormatHelper import CommonFormatHelper
from common.CommonFormatHelper import CommonObjectPrinter
from abc import ABCMeta, abstractmethod

log = CommonLogging().getLogger(__name__)
out = CommonFormatHelper()

class TeAccountInfo(CommonObjectPrinter):

    def __init__(self, json_data):

        self.accountId = json_data["aid"]
        self.accountGroupName = json_data["accountGroupName"]
        self.organizationName = json_data["organizationName"]
    
class TeTest(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def loadTestData(json_data):
        pass

class TeTestFactory():

    @staticmethod
    def create(json_data, agentType):
        testType = json_data["type"]
        errorSring="Test of type {} and agent type {} was not found".format(
            testType,
            agentType
            )

        # statement for debugging
        #if testType == "sip-server":
        #    print("agentType: {}".format(agentType))
        #    print(json_data)

        try:
            if testType == "http-server" and agentType == "test":
                return TeEnterpriseTestHttp(json_data)

            if testType == "agent-to-server" and agentType == "test":
                return TeEnterpriseTestAgent2Server(json_data)

            if testType == "bgp" and agentType == "test":
                return TeEnterpriseTestAgent2Server(json_data)

            if testType == "page-load" and agentType == "test":
                return TeEnterpriseTestPageLoad(json_data)

            if testType == "dns-trace" and agentType == "test":
                return TeEnterpriseDnsTrace(json_data)

            if testType == "agent-to-agent" and agentType == "test":
                return TeEnterpriseAgent2Agent(json_data)

            if testType == "sip-server" and agentType == "test":
                return TeEnterpriseSipServer(json_data)

            if testType == "voice" and agentType == "test":
                return TeEnterpriseVoice(json_data)

            if testType == "http-server" and agentType == "endpointTest":
                return TeEndpointTestHttp(json_data)

            if testType == "agent-to-server" and agentType == "endpointTest":
                return TeEndpointTestAgent2Server(json_data)

            raise Exception(errorSring)
        except Exception as err:
            print(err)
        return

class TeEndpointTestHttp(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

        return self

class TeEndpointTestAgent2Server(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]
        return self

class TeEnterpriseTestHttp(CommonObjectPrinter, TeTest):

    def __init__(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

class TeEnterpriseTestHttp(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

        return self

class TeEnterpriseTestAgent2Server(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

        return self

class TeEnterpriseTestBgb(CommonObjectPrinter, TeTest):

    def __init__(self,json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self,json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

        return self

class TeEnterpriseTestPageLoad(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.testId = json_data["testId"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.enabled = json_data["enabled"]
        #self.interval = json_data["interval"]
        self.testName = json_data["testName"]
        self.type = json_data["type"]

        return self

class TeEnterpriseDnsTrace(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.enabled = json_data["enabled"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.type = json_data["type"]

        return self

class TeEnterpriseAgent2Agent(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.enabled = json_data["enabled"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.type = json_data["type"]

        return self

class TeEnterpriseSipServer(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.enabled = json_data["enabled"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.type = json_data["type"]

        return self

class TeEnterpriseVoice(CommonObjectPrinter, TeTest):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadTestData(json_data)

    def loadTestData(self, json_data):

        self.enabled = json_data["enabled"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.alertsEnabled = json_data["alertsEnabled"]
        self.apiLinks = json_data["apiLinks"]
        self.type = json_data["type"]

        return self

class TeAlert(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def loadAlertData(json_data):
        pass

    @staticmethod
    @abstractmethod
    def getLink2Alert(json_data):
        pass

    @staticmethod
    @abstractmethod
    def getLink2Test(json_data):
        pass

    @staticmethod
    @abstractmethod
    def getLink2Hist(json_data):
        pass

class TeAlertFactory():

    @staticmethod
    def create(json_data, agentType):

        errorSring="Alert for agent type {} was not found".format(agentType)

        try:
            if agentType == "enterprise":
                return TeEnterpriseAlert(json_data)

            if agentType == "endpoint":
                return TeEndpointAlert(json_data)
            raise Exception(errorSring)

        except Exception as err:
            print(err)

        return

class TeEnterpriseAlert(CommonObjectPrinter, TeAlert):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadAlertData(json_data)

    def loadAlertData(self, json_data):

        print("load data")
        self.active = json_data["active"]
        self.alertId = json_data["alertId"]
        self.ruleId = json_data["ruleId"]
        self.ruleName = json_data["ruleName"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.agents = json_data["agents"]
        self.apiLinks = json_data["apiLinks"]
        self.dateStart = json_data["dateStart"]
        self.type = json_data["type"]
        self.violationcount = json_data["violationCount"]
        self.link2Alert = self.getLink2Alert()
        self.link2Test = self.getLink2Test()
        self.link2Hist = self.getLink2Hist()
        print("load data done")

    def getLink2Alert(self):
        url="https://app.thousandeyes.com/alerts/list/active?"
        if self.testId != None:
            params="testId={}&searchHasAnd=false".format(
                self.testId,
            )
            url=url+params
        return url

    def getLink2Hist(self):
        url="https://app.thousandeyes.com/alerts/list/history?"
        params=""
        if self.testId != None :
            params=params+"testId={}&".format(self.testId)
        if self.alertId != None :
            params=params+"alertId={}&".format(self.alertId)
        params=params+"timespanStart={}&".format(self.dateStart)
        params=params+"searchHasAnd=false"
        url=url+params
        return url

    def getLink2Test(self):
        if self.type == "EndpointNetworkServer":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowHttp"
        elif self.type == "EndpointPathTrace":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowNetworkTest"
        elif self.type == "Http":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowHttp"
        else:
            message = "Alert Type {} unknown".format(self.type)
            log.warn(message)
            return ""

        params ="?"
        params = params + "roundId={}&".format(self.dateStart)
        #params = params + "metric={}&".format(metric)
        params = params + "scenarioId={}&".format(scenarioId)
        params = params + "testId={}".format(self.testId)
        return url+params



class TeEndpointAlert(CommonObjectPrinter, TeAlert):

    def __init__(self, json_data) -> None:
        super().__init__()
        self.loadAlertData(json_data)

    def loadAlertData(self, json_data):
        self.active = json_data["activeState"]
        self.alertId = json_data["alertId"]
        self.ruleId = json_data["ruleId"]
        self.ruleName = json_data["ruleName"]
        self.testId = json_data["testId"]
        self.testName = json_data["testName"]
        self.dateStart = json_data["firstSeen"]
        self.type = json_data["alertType"]
        self.violationcount = json_data["violationCount"]
        self.link2Alert = self.getLink2Alert()
        self.link2Test = self.getLink2Test()
        self.link2Hist = self.getLink2Hist()
        print("Date start",self.dateStart)

    def getLink2Alert(self):
        url="https://app.thousandeyes.com/alerts/list/active?"
        if self.testId != None:
            params="testId={}&searchHasAnd=false".format(
                self.testId
            )
            url=url+params
        return url

    def getLink2Hist(self):
        url="https://app.thousandeyes.com/alerts/list/history?"
        params=""
        if self.alertId != None:
            params=params+"alertId={}&".format(self.alertId)
        if self.testId != None:
            params=params+"testId={}&".format(self.testId)
            #params=params+"timespanStart={}&".format(self.dateStart)
        params=params+"searchHasAnd=false"
        url=url+params
        return url

    def getLink2Test(self):
        if self.type == "EndpointNetworkServer":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowHttp"
        elif self.type == "EndpointPathTrace":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowNetworkTest"
        elif self.type == "Http":
            url = "https://app.thousandeyes.com/view/endpoint-agent/"
            metric = "availablity"
            scenarioId = "eyebrowHttp"
        else:
            message = "Alert Type {} unknown".format(self.alertType)
            log.warn(message)
            return ""

        params ="?"
        params = params + "roundId={}&".format(self.dateStart)
        #params = params + "metric={}&".format(metric)
        params = params + "scenarioId={}&".format(scenarioId)
        params = params + "testId={}".format(self.testId)
        return url+params

class TeAlertRule(CommonObjectPrinter):

    def __init__(self, json_data):

        self.ruleId = json_data["ruleId"]
        self.ruleName = json_data["ruleName"]
        self.alertType = json_data["alertType"]
        self.tests = json_data["tests"]
        self.notifications = json_data["notifications"]

if __name__ == "__main__":
    api = TeApiWrapper()

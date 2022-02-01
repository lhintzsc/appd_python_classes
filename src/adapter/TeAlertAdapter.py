from appd.AppdApiWrapper import AppdApiWrapper
from te.TeAlertHandler import TeAlertHandler
from te.TeAlertHandler import TeAlertSender
from loguru import logger

class LogAlertAdapter(TeAlertSender):

    def sendActiveAlerts(self, alerts):

        for alert in alerts:
            logger.info("Alert ID        : {}".format(alert.alertId))
            logger.info("Test ID         : {}".format(alert.testId))
            logger.info("Rule ID         : {}".format(alert.ruleId))
            logger.info("Rule Name       : {}".format(alert.ruleName))
            logger.info("Test Name       : {}".format(alert.testName))
            logger.info("Test Type       : {}".format(alert.type))
            logger.info("startData       : {}".format(alert.dateStart))
            logger.info("Link2Alert      : {}".format(alert.getLink2Alert()))
            logger.info("Link2Test       : {}".format(alert.getLink2Test()))
            logger.info("Link2Hist       : {}".format(alert.getLink2Hist()))
            logger.info("Violations      : {}".format(alert.violationcount))

class AppdAlertAdapter(TeAlertSender):
    def __init__(self):

        self.__api = AppdApiWrapper()
        self.__mapAppId = None
        self.__mapSeverity = None
        self.__eventType = "CUSTOM"
        self.__customEventType = "Thousand Eyes Alert Adapter"

    def getAppId(self, testId):
        appId = "8914"
        if self.__mapAppId == None:
            appId = "8914"
        return appId

    def getSeverity(self, testId, ruleId):
        severity = "INFO"
        if self.__mapSeverity == None:
            severity = "WARN"
        return severity

    def sendActiveAlerts(self, alerts):

        logger.info("AppD Alert Adapter")
        for alert in alerts: 
            self.sendAlert(alert)

    def sendAlert(self, alert):

        appId = self.getAppId(alert.testId)
        severity = self.getSeverity(alert.testId, alert.ruleId)

        summary = "TE Alert: {} -> see Comments".format(
            alert.ruleName
        )

        link2AlertText="Drill Down to Thousand Eyes"
        link2Alert = "<a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>".format(
            alert.getLink2Alert(),
            link2AlertText
        )

        link2HistText="Drill Down to Thousand Eyes"
        link2Hist = "<a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>".format(
            alert.getLink2Hist(),
            link2HistText
        )

        link2TestText="Drill Down to Thousand Eyes"
        link2Test = "<a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>".format(
            alert.getLink2Test(),
            link2TestText
        )

        comment = '''
            <p><strong>Thousand Eyes Rule Violation</strong></p>
            <table style="height: 110px; width: 642px;">
            <tbody>
            <tr>
            <td style="width: 65.1094px;">Rule Name</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Test Name</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Test Type</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Start Date</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Affected Agents</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Link to Alert</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Link to Hist</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            <tr>
            <td style="width: 65.1094px;">Link to Test</td>
            <td style="width: 348.891px;">&nbsp;{}</td>
            </tr>
            </tbody>
            </table>
        '''.format(
                alert.ruleName,
                alert.testName,
                alert.type,
                alert.dateStart,
                alert.violationcount,
                link2Alert,
                link2Hist,
                link2Test
            )

        self.__api.postEvent(
            appId=appId,
            severity=severity,
            eventtype=self.__eventType,
            customeventtype=self.__customEventType,
            summary=summary,
            comment=comment
        )

if __name__ == "__main__":

    logAdapter = LogAlertAdapter()
    appdAdapter = AppdAlertAdapter()

    handler = TeAlertHandler(appdAdapter)
    #handler = TeAlertHandler(AppdAlertAdapter)
    handler.loadConfigYml()
    handler.loadAccountInfo()
    #handler.logStateOfClass()
    #handler.loadAccountInfo()
    handler.loadTests()
    #handler.loadEndpointTests()
    #handler.loadEnterpriseTests()
    handler.loadAlertRules()
    #handler.loadActiveAlerts()
    #handler.collectAndSendActiveAlerts()
    #handler.getTestsInRules()
    handler.setWatchlist()
    #handler.deleteWatchlist()
    #print(handler.getWatchlist())
    #print(handler.isInWatchlist(1331086,2114850))
    handler.collectAndSendActiveAlerts()
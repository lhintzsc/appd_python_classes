from appd.AppdRbacHandler import AppdRbacReporter
from appd.AppdRbacHandler import AppdRbacHandler
from common.CommonFormatHelper import CommonObjectPrinter
from loguru import logger


class OpsGenieReportAdapter(AppdRbacReporter, CommonObjectPrinter):

    def __init__(
        self,
        apiWrapper,
        controllerLink,
        account,
        severity,
        message,
        description
        ) -> None:
        super().__init__(
            controllerLink,
            account,
            severity,
            message,
            description
        )

        logger.debug("Ini class: {}".format(__name__))

        self.__api = apiWrapper
        self._account = account
        self._message = message
        self._description = description
        self._severity = severity

        logger.debug("State of object: {}".format(self.show()))

    def reportUsersWoLogin(self, users, days):

        logger.info("Report users without login")

        account= self._account
        message = self._message
        priority = self._severity
        description = self._description
        controllerLink=self.__getControllerLink()
        tableOfUsers=self.__getTable(users)

        try:
            description_formated=description.format(
                account,
                days,
                controllerLink,
                tableOfUsers
            )
        except:
            logger.error("Error while formating output string")
            logger.error("                                   ")
            logger.error("- description must have 4x{} in the string")
            logger.error("- example description: account {} days {} link {} table {}")
            logger.error("- actual description: "+description)
            logger.error("- account: {}".format(account))
            logger.error("- days: {}".format(days))
            logger.error("- controllerLink: {}".format(controllerLink))
            logger.error("- tableOfUsers: {}".format(tableOfUsers))
            logger.error("                                   ")

        self.__api.postAlerts(
            message,
            description_formated,
            priority
        )
        return
        

    def __getControllerLink(self):
        link = "<a href=\"{}\" target=\"_blank\" rel=\"noopener noreferrer\">{}</a>".format(
            self._controllerLink,
            "appdynamics"
        )
        return link

    def __getTable(self, users):
        logger.info("Create HTML table for output")
        table=""
        header=""
        table=table+"<table>"
        header=header+"<thead>"
        header=header+"<th>{}</th>".format("Display")
        header=header+"<th>{}</th>".format("Name")
        header=header+"<th>{}</th>".format("E-Mail")
        header=header+"<th>{}</th>".format("SAML/LOCAL")
        header=header+"<thead>"
        table=table+header
        table=table+"<tbody>"
        logger.debug("users: {}".format(users))
        for user in users:
            if user["PROVIDER"] == "INTERNAL": user["PROVIDER"] = "LOCAL"
            row=""
            row=row+"<tr>"
            row=row+"<th>{}</th>".format(user["DISPLAY"])
            row=row+"<th>{}</th>".format(user["NAME"])
            row=row+"<th>{}</th>".format(user["EMAIL"])
            row=row+"<th>{}</th>".format(user["PROVIDER"])
            row=row+"<tr>"
            table=table+row
        table=table+"<tbody>"
        table=table+"</table>"
        logger.debug("table: {}".format(table))
        return table
        
if __name__ == "__main__":
    #test
    rbac = AppdRbacHandler(OpsGenieReportAdapter())
    rbac.reportUsersWoLogin()
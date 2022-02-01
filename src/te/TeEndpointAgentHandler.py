from dependency_injector import containers, providers
from common.CommonFormatHelper import CommonObjectPrinter
from common.CommonQuickObjectLoader import QuickObjectLoaderPickle
from common.CommonFormatHelper import CommonFormatHelper
from te.TeApiWrapper import TeApiWrapper
from pandas.core.frame import DataFrame
import logging
import pandas as pd
import json
from time import sleep

out=CommonFormatHelper()

class TeEndpointAgentHander(CommonObjectPrinter):

    def __init__(
        self,
        api,
        accountId,
        excelReport=None
    ):

        self.__logger = logging.getLogger(
            f'{__name__}.{self.__class__.__name__}',
        )
        self.__api=api
        self.__accountId=accountId
        self.__dfEndpointAgents=pd.DataFrame()
        self.__excelReport=excelReport

        self.__objectLoader = QuickObjectLoaderPickle()
        self.__objectLoader.setRefreshTime(1) # refresh time in hours
        self.__cacheDfEndpointAgents=".//cache//pickle//{}//dfEndpointAgents.pkl".format(TeEndpointAgentHander)
        self.__iniDataframes()

    def __iniDataframes(self):
        print("iniData")
        self.__dfEndpointAgents = self.__objectLoader.load(
            self.__cacheDfEndpointAgents,
            self.__getEndpointAgents,
            {}
        )
        print("Test2")

    def __getEndpointAgents(self):
        response = self.__api.getAllEndpointAgents(self.__accountId)
        agents = response["endpointAgents"]
        agentList = []
        for agent in agents:
            agentDict = {}
            for client in agent["clients"]:
                agentDict = {
                    "AGENT_ID": agent["agentId"],
                    "NAME_USER": client["userProfile"]["userName"],
                    "NAME_AGENT": agent["agentName"],
                    "NAME_COMPUTER": agent["computerName"],
                    "VERSION_OS": agent["osVersion"],
                    "VERSION_KERNEL": agent["kernelVersion"],
                    "VERSION_AGENT": agent["version"],
                    "MANUFACTURER": agent["manufacturer"],
                    "MODEL": agent["model"],
                    "LAST_SEEN": agent["lastSeen"],
                    "STATUS": agent["status"],
                    "LOCATION": agent["location"]["locationName"],
                }
                agentList.append(agentDict)

        dfEndpointAgents = pd.DataFrame(agentList)
        return dfEndpointAgents.copy()

    def writeRbacExcel(self):
        '''
        Write excel file that contains basic user inforamtion, the mapping from users to roles and goups. 
        Finally, it shows users that did not connect to the account for x number of days.
        '''
        self.__iniDataframes()
        # write user information to excel
        self.__logger.info("Write agent information to file: {}".format(self.__excelReport))
        with pd.ExcelWriter(self.__excelReport) as writer:  
            self.__dfEndpointAgents.to_excel(writer, merge_cells=False, sheet_name='Agent Info')
        return






class TeEndpointAgentHandlerContainer(containers.DeclarativeContainer):

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

    teEndpointAgentHandler = providers.Factory(
        TeEndpointAgentHander,
        api=teApiWrapper,
        accountId=219516,
        excelReport="./TeAgentReport.xlsx"
    )

if __name__ == "__main__":

    container=TeEndpointAgentHandlerContainer()
    container.config.from_yaml('./config.yml')

    #api = container.teApiWrapper()
    #out.print(api.getAllEndpointAgents(219516))
    handler=container.teEndpointAgentHandler()
    handler.writeRbacExcel()


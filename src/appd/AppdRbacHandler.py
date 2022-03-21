from datetime import datetime, timedelta
from pandas.core.frame import DataFrame
from common.CommonFormatHelper import CommonObjectPrinter
from common.CommonQuickObjectLoader import QuickObjectLoaderPickle
from abc import ABCMeta, abstractmethod
from loguru import logger
import pandas as pd
import progressbar
from time import sleep

class AppdRbacReporter(CommonObjectPrinter,metaclass=ABCMeta):

    def __init__(
        self,
        controllerLink,
        account,
        severity,
        message,
        description
        ) -> None:

        self._controllerLink=controllerLink
        self._account=account
        self._severity =severity
        self._message =message
        self._description =description

        return

    @abstractmethod
    def reportUsersWoLogin(self, users, days):
        pass

class DummyReportAdapter(AppdRbacReporter):

    def __init__(
        self,
        controllerLink=None,
        account=None,
        severity=None,
        message=None,
        description=None
        ) -> None:
        super().__init__(
            controllerLink,
            account,
            severity,
            message,
            description
        )

    def reportUsersWoLogin(self, users, days):
        logger.debug("Report users without login DUMMY")


class AppdRbacHandler(CommonObjectPrinter):

    def __init__(
        self, 
        apiWrapper,
        rbacReportAccount,
        rbacReportDays,
        reportAdapter=DummyReportAdapter(),
        rbacReportExcel=None,
    ):

        # ini dependencies and default values
        logger.info("Ini class: {}".format(__name__))

        self.__reporter = reportAdapter
        self.__api = apiWrapper
        self.__dfUsers = pd.DataFrame()
        self.__dfDetails = pd.DataFrame()
        self.__dfUsersAndLogins = pd.DataFrame()
        self.__rbacReport = {}
        self.__rbacReportAccount = rbacReportAccount
        self.__rbacReportDays = rbacReportDays
        self.__rbacReportExcel = rbacReportExcel

        self.__objectLoader = QuickObjectLoaderPickle()
        self.__objectLoader.setRefreshTime(1) # refresh time in hours
        self.__cacheDfUsers=".//cache//pickle//{}//dfUsers.pkl".format(AppdRbacHandler)
        self.__cacheDfUserDetails=".//cache//pickle//{}//dfDetails.pkl".format(AppdRbacHandler)
        self.__cacheRbacReport=".//cache//pickle//{}//rbacReport.pkl".format(AppdRbacHandler)

        logger.debug("State of object: {}".format(self.show()))

        return

    def __getUsers(self):
        '''
        Collect all users in the system
        '''
        logger.info("Collect user info")
        dfUsers = pd.DataFrame()
        users = self.__api.getAllUsers()["users"]
        dfUsers = dfUsers.from_dict(users)
        dfUsers.columns = ["ID","NAME"]
        dfUsers = dfUsers.set_index("ID")
        return dfUsers.copy()

    def __getRolesFromDetails(self,details):
        '''
        Gather RBAC roles for all users
        '''
        try:
            roles = details["roles"]
            id = details["id"]
            df = DataFrame.from_dict(roles)
            df = df.drop(['id'], axis=1)
            df.insert(0, 'ID', id)
            df.insert(1, 'TYPE', "ROLE")
            df.columns = ["ID", "TYPE", "R/G-NAME"]
            df = df.set_index("ID")
            return df.copy()
        except KeyError:
            return None

    def __getGroupsFromDetails(self, details):
        '''
        Gather RBAC groups for all users
        '''
        try:
            groups = details["groups"]
            id = details["id"]
            df = DataFrame.from_dict(groups)
            df = df.drop(['id'], axis=1)
            df.insert(0, 'ID', id)
            df.insert(1, 'TYPE', "GROUP")
            df.columns = ["ID", "TYPE", "R/G-NAME"]
            df = df.set_index("ID")
            return df.copy()
        except KeyError:
            return None
        
    def __getUserInfo(self, details):
        '''
        Return dataframe object for basic user information
        '''
        try:
            dictCol = {}
            columns = ["NONE","NONE","NONE","NONE"]
            columns[0] = details["name"]
            columns[1] = details["email"]
            columns[2] = details["displayName"]
            columns[3] = details["security_provider_type"]
            dictCol[details['id']] = columns
            df = DataFrame.from_dict(dictCol,orient='index')
            df.columns = ["NAME", "EMAIL","DISPLAY","PROVIDER"]
            return df.copy()
        except KeyError:
            return None

    def __getUserDetails(self):
        '''
        Download user datails and RBAC information from appdynamics controller
        and join both information together in a dataframe object.
        '''
        # empty dataframe
        allUserDetails = pd.DataFrame(columns=["NAME","EMAIL","DISPLAY","PROVIDER"])
        rolesAndGroups = pd.DataFrame(columns=["TYPE", "R/G-NAME"])
        #rolesAndGroups.columns = ["ID", "TYPE", "R/G-NAME"]
        # get ids for iteration
        ids = self.__dfUsers.index
        # ini values and progressbar
        bar = progressbar.ProgressBar(
            maxval=len(ids), \
            widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()] \
        )
        cnt = 0
        allDetails=[]
        allGroups=[]
        # start download of user details
        logger.info("Download user details for {} users:".format(ids.size))
        bar.start()
        for i in ids:
            roles=None
            groups=None
            userDetails = None
            details = self.__api.getUserDetails(i)
            # get roles and group
            roles = self.__getRolesFromDetails(details)
            groups = self.__getGroupsFromDetails(details)
            userDetails = self.__getUserInfo(details)
            # append to roles and group data frame
            rolesAndGroups = rolesAndGroups.append(groups)
            rolesAndGroups = rolesAndGroups.append(roles)
            allUserDetails = allUserDetails.append(userDetails)
            cnt = cnt +1
            bar.update(cnt)
        bar.finish()
        # join user and rbac info
        dfDetails = allUserDetails.join(rolesAndGroups, how="left")
        dfDetails.set_index(["NAME","PROVIDER"],inplace=True)

        return dfDetails.copy()

    
    def __getTimeIntervals(self, startTime, endTime):
        '''
        Function that devides a time range into time intervals of 1 days. Start and end-date are datetime objects
        '''
        logger.info("Calculate time intervals")
        # set time of date to standard value
        startTime = startTime.replace(hour=00, minute=00, second=00)
        endTime = endTime.replace(hour=23, minute=59, second=59)
        # handle exceptions
        if endTime >= datetime.now():
            errorOutput="Endtime {} must be before today {}".format(endTime,datetime.now())
            raise ValueError(errorOutput)
        elif startTime > endTime:
            errorOutput="StartTime {} must be before EndTime {}".format(startTime, endTime)
            raise ValueError(errorOutput)
        
        timeDifference = endTime - startTime
        nIntervals = timeDifference.days+1

        intervals = []
        start = startTime
        for i in range(0,nIntervals):
            interval = {}
            interval["number"] = i+1
            interval["startTime"] = (start + timedelta(days=i)).replace(hour=00, minute=00, second=00)
            interval["endTime"] = (start + timedelta(days=i)).replace(hour=23, minute=59, second=59)
            start = start.replace(hour=23, minute=59, second=59)
            intervals.append(interval)

        logger.debug("startTime    :{}".format(startTime))
        logger.debug("endTime      :{}".format(endTime))
        logger.debug("intervals    :{}".format(intervals))

        return intervals

    def __getLastLogin(self, startTime, endTime):
        '''
        Collect all login information between a certain time interval
        '''
        # ini REST request parameter
        intervals = self.__getTimeIntervals(startTime, endTime)
        includeLogin="action:LOGIN"
        # collect login data over several 1 day time intervals
        logins = []
        log_format = "Request Audit Interval {} : from {} to {}"
        for interval in intervals:
            log_output = log_format.format(
                interval["number"],
                interval["startTime"],
                interval["endTime"]
            )
            logger.info(log_output)
            temp=self.__api.getControllerAuditHistory(
                startTime=interval["startTime"], 
                endTime=interval["endTime"],
                include=includeLogin
            )
            logins = logins + temp
        # create dataframe drop and rename columns
        dfLogins = pd.DataFrame().from_records(logins)
        #dfLogins.drop(["objectId","action","apiKeyId","apiKeyName"] ,axis=1,inplace=True)
        
        logger.debug(dfLogins.columns)
        dfLogins.drop(
            dfLogins.columns.difference(['timeStamp', 'auditDateTime', 'accountName', 'securityProviderType', 'userName']),
            axis=1,
            inplace=True
        )
        logger.debug(dfLogins.columns)

        dfLogins.columns = ["TIMESTAMP","LOGINTIME","ACCOUNT","PROVIDER","NAME"]
        # get lastest login date only
        dfLogins.set_index(["NAME","PROVIDER"],inplace=True)
        dfLogins = dfLogins.groupby(level=0,group_keys=None).apply(lambda x: x.loc[x['TIMESTAMP']==x['TIMESTAMP'].max()]).copy()
        dfLogins["LOGINTIME"] = dfLogins.apply(
            lambda x:
                x['LOGINTIME'] if pd.isnull(x['LOGINTIME'])\
                        else datetime.strptime(str(x["LOGINTIME"])[:19],"%Y-%m-%dT%H:%M:%S"),
                axis=1
        )
        # return result
        return dfLogins.copy()

    def __getLoginInfoFor(self):
        '''
        Starting from yesterday, get login information for the last x days.
        '''
        logger.info("Get login info for the last x+1 days")
        days = int(self.__rbacReportDays)
        account = self.__rbacReportAccount

        # ini dataframes
        dfLogins = pd.DataFrame()
        dfUsersAndLogins = pd.DataFrame()
        # ini dates
        yesterday = datetime.now() - timedelta(days=1)
        startTime = yesterday - timedelta(days=days)
        # ini login data for one ore multiple accounts
        dfLogins = self.__getLastLogin(startTime, yesterday)
        if account==None:
            pass
        else:
            mask = dfLogins["ACCOUNT"] == account
            dfLogins = dfLogins[mask].copy()

        dfUsersAndLogins = self.__dfDetails.join(dfLogins, how="left")
        
        dfUsersAndLogins["DAYS W/O LOGIN"] = dfUsersAndLogins.apply(
            lambda x:
                days+1 if pd.isnull(x['LOGINTIME'])\
                        else (datetime.now() - x["LOGINTIME"]).days,
                axis=1
        )
        self.__dfUsersAndLogins = dfUsersAndLogins

        return dfUsersAndLogins.copy()

    def __getUsersWoLoginFor(self):
        '''
        Get users that did not login for x days.
        '''
        logger.info("Get users w/o login")
        days=int(self.__rbacReportDays)
        # ini dataframe
        usersWoLogin = pd.DataFrame()
        # select users
        mask = self.__dfUsersAndLogins["DAYS W/O LOGIN"] > days
        usersWoLogin = self.__dfUsersAndLogins.loc[mask]
        # filter for output
        usersWoLogin = usersWoLogin.drop(["TYPE","R/G-NAME"],axis=1)
        # return output
        return usersWoLogin.copy()

    def __iniDataframes(self):
        logger.debug("ini dfUsers")
        self.__dfUsers = self.__objectLoader.load(
            self.__cacheDfUsers,
            self.__getUsers,
            {}
        )
        logger.debug("ini dfUserDetails")
        self.__dfDetails = self.__objectLoader.load(
            self.__cacheDfUserDetails,
            self.__getUserDetails,
            {}
        )

    def __iniRbacReport(self):
        logger.debug("ini RBAC Report")
        self.__rbacReport = self.__objectLoader.load(
            self.__cacheRbacReport,
            self.__getRbacReport,
            {}
        )

    def deleteCache(self):
        self.__objectLoader.deleteCache(self.__cacheDfUsers)
        self.__objectLoader.deleteCache(self.__cacheDfUserDetails)
        self.__objectLoader.deleteCache(self.__cacheRbacReport)

    def __getRbacReport(self):
        logger.info("Create RBAC report")
        # empty dataframes to write output excel
        userInfo = pd.DataFrame()
        userRoles = pd.DataFrame()
        userWoLogin = pd.DataFrame()
        self.__iniDataframes()
        # enhance user inforamtion with login information
        userInfo = self.__getLoginInfoFor()
        userRoles = userInfo.copy()
        userWoLogin = self.__getUsersWoLoginFor()
        # clean user info
        userInfo = userInfo.drop(["TYPE","R/G-NAME","ACCOUNT","TIMESTAMP","DAYS W/O LOGIN"],axis=1).copy()
        userInfo.reset_index(inplace=True)
        userInfo = userInfo.drop_duplicates()
        # clean user roles
        userRoles = userRoles.drop(["EMAIL","DISPLAY","ACCOUNT","LOGINTIME","TIMESTAMP","DAYS W/O LOGIN"],axis=1).copy()
        userRoles.reset_index(inplace=True)
        userRoles = userRoles.drop_duplicates()
        # clean users w/o login
        userWoLogin = userWoLogin.drop(["ACCOUNT","TIMESTAMP"],axis=1).copy()
        userWoLogin.reset_index(inplace=True)
        userWoLogin = userWoLogin.drop_duplicates()

        rbacReport = { "userInfo": userInfo, "userRoles": userRoles, "userWoLogin": userWoLogin }

        return rbacReport

    def writeRbacExcel(self):
        '''
        Write excel file that contains basic user inforamtion, the mapping from users to roles and goups. 
        Finally, it shows users that did not connect to the account for x number of days.
        '''
        self.__iniDataframes()
        self.__iniRbacReport()
        # write user information to excel
        logger.info("Write user information to file: {}".format(self.__rbacReportExcel))
        with pd.ExcelWriter(self.__rbacReportExcel) as writer:  
            self.__rbacReport["userInfo"].to_excel(writer, merge_cells=False, sheet_name='User Info')
            self.__rbacReport["userRoles"].to_excel(writer, merge_cells=False, sheet_name='User Roles')
            self.__rbacReport["userWoLogin"].to_excel(writer, merge_cells=False, sheet_name='Users without Login')
        return

    def reportUsersWoLogin(self):
        '''
        send users without login for x days
        '''
        logger.info("Report users w/o login")
        self.__iniDataframes()
        self.__iniRbacReport()

        usersWoLogin=self.__rbacReport["userWoLogin"]
        users=[]

        for index, row in usersWoLogin.iterrows():
            user = {}
            user["NAME"] = row["NAME"]
            user["EMAIL"] = row["EMAIL"]
            user["PROVIDER"] = row["PROVIDER"]
            user["DISPLAY"] = row["DISPLAY"]
            users.append(user)

        logger.debug("users: {}".format(users))
        logger.debug("int(self.__rbacReportDays)-1={}".format(int(self.__rbacReportDays)-1))
        self.__reporter.reportUsersWoLogin(users, int(self.__rbacReportDays)-1)
        return


if __name__ == "__main__":
    rbac = AppdRbacHandler(DummyReportAdapter())
    rbac.reportUsersWoLogin()
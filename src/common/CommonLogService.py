from dependency_injector import containers, providers
from common.CommonFormatHelper import CommonObjectPrinter
from loguru import logger
import time
import datetime
import sys

logger.remove()

class LogSettings(CommonObjectPrinter):

    def __init__(
        self,
        sink,
        format,
        level,
        refreshFlag,
        refreshRate,
        modules
    ):
        logger.info("Ini class: {}".format(__name__))

        self.sink = self._getSink(sink)
        self.format = format
        self.level = level
        self.refreshFlag = refreshFlag
        self.refreshRate = self._getRefreshRate(refreshRate)
        self.modules = modules

        logger.debug("State of object: {}".format(self.show()))

        return

    def _getRefreshRate(self,seconds):
        return datetime.timedelta(seconds=int(seconds))

    def _getSink(self, sink):
        if sink == "sys.stdout":
            return sys.stdout
        elif sink == "sys.stderr":
            return sys.stderr
        else:
            return sink

class SettingsContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    logSettings = providers.Singleton(
        LogSettings,
        sink = config.LogSettings.sink,
        format = config.LogSettings.format,
        level = config.LogSettings.level,
        refreshFlag = config.LogSettings.refreshFlag,
        refreshRate = config.LogSettings.refreshRate,
        modules = config.LogSettings.modules
    )

class CommonLogService(CommonObjectPrinter):

    def __init__(
        self,
        logConfig
    ):

        logger.debug("Ini class: {}".format(__name__))

        self.__logConfig = logConfig
        self.__container = SettingsContainer()
        self.__settings = None
        self.__lastRefresh = None
        self.refresh()

        logger.debug("State of object: {}".format(self.show()))
        return

    def _iniFromConfig(self):
        self.__container.config.from_yaml(self.__logConfig)
        self.__settings = self.__container.logSettings()
        return

    def _setModules(self):
        for lib, flag in self.__settings.modules.items():
            if flag == True:
                logger.debug("LOGGING ON : {} = {}".format(lib, flag))
                logger.enable(lib)
            else:
                logger.debug("LOGGING OFF: {} = {}".format(lib, flag))
                logger.disable(lib)
    
    def refresh(self):
        if self._timeToRefresh():
            self._iniFromConfig()
            logger.remove()
            logger.add(
                sink=self.__settings.sink,
                colorize=True,
                format=self.__settings.format,
                level=self.__settings.level
            )
            self._setModules()
            self.__lastRefresh = datetime.datetime.now()
            logger.info(
                "LOGGING: level = {}, refreshRate = {}".format(
                    self.__settings.level,
                    self.__settings.refreshRate
            ))
            logger.debug("State of object: {}".format(self.show()))
        else:
            pass

    def _timeToRefresh(self):
        if self.__lastRefresh == None:
            return True
        elif self.__settings.refreshFlag == False\
        and self.__lastRefresh != None:
            return False
        elif self.__settings.refreshFlag == True\
        and self.__lastRefresh != None:
            timeDiff = self._getTimeDiff()
            if (timeDiff) < self.__settings.refreshRate:
                return False
            else:
                return True
        else:
            logger.warning("No matching condition for:")
            logger.warning("refreshFlag:    {}".format(self.__settings.refreshFlag))
            logger.warning("lastRefresh:    {}".format(self.__lastRefresh))

    def _getTimeDiff(self):
        curTime = datetime.datetime.now()
        modTime = self.__lastRefresh
        try:
            timeDiff = curTime - modTime
            logger.debug("Type: {} and curTime:  {}".format(type(curTime), curTime))
            logger.debug("Type: {} and modTime:  {}".format(type(modTime), modTime))
            logger.debug("Type: {} and timeDiff: {}".format(type(timeDiff), timeDiff))
            return timeDiff
        except:
            logger.warning("Operation not supported timeDiff = curTime-modTime for values:")

if __name__ == "__main__":


    logService = CommonLogService("./logging.yaml")

    logger.info("INFO Message")
    logger.debug("DEBUG Message")

    #logger.remove()
    #logger.add(sink=sys.stdout,level="INFO")

    #logger.remove()
    #logger.add(sink=sys.stdout,level="INFO")

    time.sleep(20)

    logService.refresh()

    time.sleep(20)

    logService.refresh()

    logger.info("INFO")
    logger.debug("DEBUG")

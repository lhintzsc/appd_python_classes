from common.CommonBackgroundJob import CommonJobAdapter
from common.CommonFormatHelper import CommonObjectPrinter
from appd.AppdRbacHandler import AppdRbacHandler
from loguru import logger



class JobAdapterAppdRbacHandler(CommonJobAdapter, CommonObjectPrinter):
    
    def __init__(
        self,
        handler: AppdRbacHandler
    ) -> None:
        logger.debug("Ini class: {}".format(__name__))

        CommonJobAdapter.__init__(self)
        self.__handler = handler

    def runJob(self):
        logger.info("runJob")
        self.__handler.reportUsersWoLogin()
        return




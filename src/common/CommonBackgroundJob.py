from common.CommonFormatHelper import CommonObjectPrinter
from common.CommonLogService import *
from apscheduler.schedulers.background import BackgroundScheduler
from abc import ABCMeta, abstractmethod

import time
import os

class CommonJobAdapter(CommonObjectPrinter,metaclass=ABCMeta):

    def __init__(self) -> None:
        return

    @abstractmethod
    def runJob(self):
        pass

class DummyJobAdapter(CommonJobAdapter):

    def __init__(self) -> None:
        super().__init__()

    def runJob(self):
        logger.info("Run dummy job")

class CommonBackgroundJob(CommonObjectPrinter):

    def __init__(
        self,
        trigger,
        dayOfWeek,
        hour,
        minute,
        timezone,
        days="0",
        hours="0",
        minutes="0",
        seconds="0",
        jobAdapter=DummyJobAdapter(),
        logService=CommonLogService("./logging.yaml")
    ):

        logger.debug("Ini class: {}".format(__name__))

        self.__jobAdapter=jobAdapter
        self.__trigger=str(trigger)
        self.__dayOfWeek=dayOfWeek
        self.__hour=hour
        self.__minute=minute
        self.__timezone=timezone
        self.__days=days
        self.__hours=hours
        self.__minutes=minutes
        self.__seconds=seconds
        self.__service=self.__getService()
        self.__logService=logService

        logger.debug("State of object: {}".format(self.show()))

    def __getService(self):
        service=BackgroundScheduler(timezone=self.__timezone)
        if self.__trigger == "cron":
            service.add_job(
                func=self.__jobAdapter.runJob,
                trigger=self.__trigger,
                day_of_week=self.__dayOfWeek, 
                hour=self.__hour, 
                minute=self.__minute,
                timezone=self.__timezone
            )
            infoMessage="CRON JOB | days of week: {}, hour: {}, minute: {}, timezone: {}".format(
                self.__dayOfWeek,
                self.__hour,
                self.__minute,
                self.__timezone
            )
            logger.info(infoMessage)
        elif self.__trigger == "interval":
            service.add_job(
                func=self.__jobAdapter.runJob,
                trigger=self.__trigger,
                days=int(self.__days),
                hours=int(self.__hours),
                minutes=int(self.__minutes),
                seconds=int(self.__seconds)
            )
            infoMessage="INTERVAL JOB | {} days, {} hours, {} min, {} sec".format(
                self.__days,
                self.__hours,
                self.__minutes,
                self.__seconds
            )
            logger.info(infoMessage)
        else:
            logger.error("Trigger {} not found: ".format(self.__trigger))
        return service

    def start(self):
        logger.info("Start background job")
        self.__service.start()
        logger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
                self.__logService.refresh()
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            self.__service.shutdown()
        pass

if __name__ == "__main__":
    service = CommonBackgroundJob(
        trigger="cron",
        dayOfWeek="tue",
        hour="22",
        minute="19",
        timezone="Europe/Berlin"
    )
    service.start()
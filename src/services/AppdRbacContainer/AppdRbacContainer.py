# dependency incjection framework
from dependency_injector import containers, providers
# module sources
from common.CommonBackgroundJob import CommonBackgroundJob
from common.CommonLogService import CommonLogService
from adapter.AppdRbacReportAdapter import OpsGenieReportAdapter
from adapter.CommonJobAdapter import JobAdapterAppdRbacHandler
from appd.AppdRbacHandler import AppdRbacHandler
from appd.AppdApiWrapper import AppdApiWrapper
from opsgenie.OpsGenieApiWrapper import OpsGenieApiWrapper
from loguru import logger
# standard modules
import os


# service dependencies
class AppdRbacContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    appdApiWrapper = providers.Singleton(
        AppdApiWrapper,
        protocol=config.AppdApiWrapper.protocol,
        controller=config.AppdApiWrapper.controller,
        account=config.AppdApiWrapper.account,
        port=config.AppdApiWrapper.port,
        apiUser=config.AppdApiWrapper.apiUser,
        apiSecret=config.AppdApiWrapper.apiSecret,
        encryption=config.AppdApiWrapper.encryption
    )

    opsGenieApiWrapper = providers.Factory(
        OpsGenieApiWrapper,
        apiKey=config.OpsGenieApiWrapper.apiKey,
        apiDomain=config.OpsGenieApiWrapper.apiDomain,
        encryption=config.OpsGenieApiWrapper.encryption
    )

    opsGenieReportAdapter = providers.Singleton(
        OpsGenieReportAdapter,
        apiWrapper=opsGenieApiWrapper,
        controllerLink=config.OpsGenieReportAdapter.controllerLink,
        account=config.OpsGenieReportAdapter.account,
        severity=config.OpsGenieReportAdapter.severity,
        message=config.OpsGenieReportAdapter.message,
        description=config.OpsGenieReportAdapter.description
    )

    appdRbacHandler = providers.Singleton(
        AppdRbacHandler,
        apiWrapper=appdApiWrapper,
        rbacReportAccount=config.AppdRbacHandler.rbacReportAccount,
        rbacReportDays=config.AppdRbacHandler.rbacReportDays,
        reportAdapter=opsGenieReportAdapter
    )

    jobAdapterAppdRbacHandler=providers.Singleton(
        JobAdapterAppdRbacHandler,
        handler=appdRbacHandler
    )

    commonLogService=providers.Factory(
        CommonLogService,
        logConfig=config.CommonLogService.logConfig
    )

    commonBackgroundJob=providers.Singleton(
        CommonBackgroundJob,
        trigger=config.CommonBackgroundJob.trigger,
        dayOfWeek=config.CommonBackgroundJob.dayOfWeek,
        hour=config.CommonBackgroundJob.hour,
        minute=config.CommonBackgroundJob.minute,
        timezone=config.CommonBackgroundJob.timezone,
        days=config.CommonBackgroundJob.days,
        hours=config.CommonBackgroundJob.hours,
        minutes=config.CommonBackgroundJob.minutes,
        seconds=config.CommonBackgroundJob.seconds,
        jobAdapter=jobAdapterAppdRbacHandler,
        logService=commonLogService
    )


if __name__ == "__main__":
    container = AppdRbacContainer()
    logger.info(os.getcwd())
    if os.path.exists('./config.yml'):
        logger.info("read config.yml")
        container.config.from_yaml('./config.yml')
    else:
        logger.info("read config.yaml")
        container.config.from_yaml('./config.yaml')
    #obj = container.appdApiWrapper()
    #obj = container.opsGenieApiWrapper()
    #obj = container.opsGenieReportAdapter()
    #obj = container.appdRbacHandler()
    #obj = container.jobAdapterAppdRbacHandler()
    service = container.commonBackgroundJob()
    service.start()
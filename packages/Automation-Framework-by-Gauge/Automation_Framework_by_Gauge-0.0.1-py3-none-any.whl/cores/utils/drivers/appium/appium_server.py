from appium.webdriver.appium_service import AppiumService

# Local
from cores.utils.common.store_util import GetUtil, StoreUtil
from cores.utils.common.time_util import TimeUtil
from cores.utils.logger_util import logger

from cores.const.mobile import AppiumConst
from cores.const.common import TimeConst


class AppiumServer:
    @staticmethod
    def start():
        logger.info("Starting Appium Server...")
        appium_config = GetUtil.suite_get(AppiumConst.Server.OBJ)
        appium_service = AppiumService()
        timer = 0
        while timer <= TimeConst.Timeout.TIMEOUT_60:
            args = ['--use-plugins', 'execute-driver',
                    '--log', 'appium_log.log',
                    '--log-level', 'debug']
            appium_service.start(address=appium_config.get(AppiumConst.Server.SERVER),
                                 p=appium_config.get(
                                     AppiumConst.Server.SERVER_PORT),
                                 args=args)
            TimeUtil.short_sleep()
            if appium_service.is_running:
                StoreUtil.suite_store(
                    AppiumConst.Server.SERVICE, appium_service)
                logger.info("Started Appium Server!")
                return True
            else:
                timer += 5
        logger.info("Can't start Appium Server!")
        return False

    @staticmethod
    def is_running():
        return GetUtil.suite_get(AppiumConst.Server.SERVICE).is_running

    @staticmethod
    def stop():
        logger.info("Stopping Appium Server...")
        timer = 0
        while timer <= TimeConst.Timeout.TIMEOUT_60:
            GetUtil.suite_get(AppiumConst.Server.SERVICE).stop()
            TimeUtil.short_sleep()
            if AppiumServer.is_running():
                timer += 5
            else:
                logger.info("Stopped Appium Server!")
                return True
        logger.info("Can't stop Appium Server!")
        return False

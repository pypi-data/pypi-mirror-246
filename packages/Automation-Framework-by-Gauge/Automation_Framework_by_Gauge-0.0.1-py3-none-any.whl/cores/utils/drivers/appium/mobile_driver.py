from appium import webdriver

from cores.const.mobile import AppiumConst, DesiredCapabilitiesConst, DeviceConst
from cores.utils.common.store_util import GetUtil


class DriverAppiumUtil:

    @staticmethod
    def create_appium_driver(platform_name: str, device_name: str, app_package: str,
                             app_activity: str, automation_name: str, platform_version: str = None,
                             bundle_id: str = None, timeout: int = 30000):
        support_version = dict(
            zip([DeviceConst.Android.ANDROID, DeviceConst.iOS.IOS], [DeviceConst.Android.SUPPORT_VERSION, DeviceConst.iOS.SUPPORT_VERSION]))

        if platform_name in [DeviceConst.Android.ANDROID, DeviceConst.iOS.IOS]:
            if platform_version in support_version[platform_name]:
                desired_caps = {
                    DesiredCapabilitiesConst.PLATFORM_NAME: platform_name,
                    DesiredCapabilitiesConst.PLATFORM_VERSION: platform_version,
                    DesiredCapabilitiesConst.DEVICE_NAME: device_name,
                    DesiredCapabilitiesConst.NEW_COMMAND_TIMEOUT: timeout,
                    DesiredCapabilitiesConst.AUTOMATION_NAME: automation_name
                }
                try:
                    if platform_name == DeviceConst.Android.ANDROID:
                        desired_caps[DesiredCapabilitiesConst.APP_PACKAGE] = app_package
                        desired_caps[DesiredCapabilitiesConst.APP_ACTIVITY] = app_activity
                    else:
                        desired_caps[DesiredCapabilitiesConst.BUNDLE_ID] = bundle_id
                    return webdriver.Remote(GetUtil.suite_get(AppiumConst.Server.OBJ).get(AppiumConst.Server.REMOTE_PATH),
                                            desired_caps)
                except Exception as ex:
                    raise ex
            else:
                raise Exception(
                    f'Do not support this version for platform {platform_name}')
        else:
            raise Exception(f'Not support this platform {platform_name}')

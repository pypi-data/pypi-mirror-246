import os
import configparser
from functools import wraps

from cores.utils.common.store_util import StoreUtil
from cores.utils.common.path_util import PathUtil
from cores.utils.common.string_util import StringUtil
from cores.utils.drivers.appium.virtual_device_util import VirtualDeviceUtil


from cores.model import DbConn

from cores.const.common import EnvironmentConst as const
from cores.const.mobile import AppiumConst, DeviceConst


def parse_db_config(db_type: str):
    """_summary_

    Args:
        db_type (str): _description_
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            config = configparser.RawConfigParser()
            config.read(PathUtil.join_prj_root_path(
                const.ConfigPath.DB_CONFIG))
            _p = {'db_name': config[db_type].get(const.Database.DB_NAME),
                  'db_host': config[db_type].get(const.Database.DB_HOST),
                  'db_port': config[db_type].get(const.Database.DB_PORT),
                  'db_username': os.getenv(const.Database.DB_USERNAME),
                  'db_pwd': StringUtil.base64_encode_text(os.getenv(const.Database.DB_PWD))
                  }
            db_obj: DbConn = DbConn(**_p)
            StoreUtil.suite_store(
                const.Database.DB_OBJ, db_obj)
            function(*args, **kwargs)
        return wrapper
    return decorator


def parse_driver_config(platform_name: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            appium_config_path = PathUtil.get_prj_root_path(
            ) + const.ConfigPath.APPIUM_CONFIG_PATH
            device_config_path = PathUtil.get_prj_root_path(
            ) + const.ConfigPath.DEVICE_CONFIG_PATH % {'name': platform_name}

            appium_config = configparser.RawConfigParser()
            appium_config.read(appium_config_path)
            device_config = configparser.RawConfigParser()
            device_config.read(device_config_path)
            if DeviceConst.iOS.IOS in platform_name:
                StoreUtil.suite_store(DeviceConst.iOS.UDID, VirtualDeviceUtil.get_supported_udid(
                    os_version=os.getenv(
                        key=AppiumConst.Client.PLATFORM_VERSION),
                    device_model=os.getenv(key=AppiumConst.Client.DEVICE_NAME)))

            StoreUtil.suite_store(AppiumConst.Server.OBJ,
                                  appium_config[AppiumConst.Server.OBJ])
            StoreUtil.suite_store(
                DeviceConst.OBJ, device_config[platform_name])

            function(*args, **kwargs)

        return wrapper

    return decorator


def parse_app_config(app_name: str):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            file = PathUtil.get_prj_root_path(
            ) + const.ConfigPath.APP_CONFIG_PATH % {'name': app_name}
            config = configparser.RawConfigParser()
            config.read(file)
            StoreUtil.suite_store(
                const.Environment.CONFIG_APP_OBJ, config[app_name])
            function(*args, **kwargs)

        return wrapper

    return decorator

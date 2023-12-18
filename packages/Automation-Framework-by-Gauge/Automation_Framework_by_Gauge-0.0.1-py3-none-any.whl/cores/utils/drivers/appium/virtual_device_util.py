import os
from typing import Dict


from cores.utils.common.store_util import GetUtil, StoreUtil
from cores.utils.common.time_util import TimeUtil
from cores.utils.common.path_util import PathUtil
from cores.utils.common.json_util import JsonConverterUtil
from cores.utils.logger_util import logger

from cores.const.common import TimeConst,  EnvironmentConst, PathConst
from cores.const.mobile import DeviceConst, CommandConst, AppiumConst


class VirtualDeviceUtil:
    @staticmethod
    def start(platform: str):
        return VirtualDeviceUtil.start_android() if platform == DeviceConst.Android.ANDROID else VirtualDeviceUtil.start_ios()

    @staticmethod
    def start_android():
        emulator_conf = GetUtil.suite_get(DeviceConst.OBJ)
        active_user = GetUtil.suite_get(
            EnvironmentConst.Environment.ENV_OBJ).active_user
        emulator_path = emulator_conf.get(CommandConst.ADB.EMULATOR_PATH) % {
            'username': active_user}
        adb_path = emulator_conf.get(CommandConst.ADB.ADB_PATH) % {
            'username': active_user}

        os.environ[DeviceConst.Android.HOME] = emulator_conf.get(
            DeviceConst.Android.HOME_PATH) % {'username': active_user}
        os.popen(emulator_path + CommandConst.ADB.START_EMULATOR %
                 {'device_name': os.getenv(AppiumConst.Client.DEVICE_NAME)})

        timer = 0
        time_out = 3
        while timer <= TimeConst.Timeout.TIMEOUT_60:
            TimeUtil.short_sleep(sleep_tm=time_out)
            active_devices = \
                os.popen(adb_path + CommandConst.ADB.LIST_DEVICES).read().replace('\t',
                                                                                  ' ').split("\n", 1)[1].split()
            if 'device' in active_devices:
                StoreUtil.suite_store(
                    DeviceConst.Android.EMULATOR_NAME, active_devices[0])
                TimeUtil.short_sleep(sleep_tm=time_out)
                return True
            else:
                timer += time_out
        return False

    @staticmethod
    def start_ios():
        udid = GetUtil.suite_get(DeviceConst.iOS.UDID)
        # boot device
        logger.info(f'Boot the simulator {udid}')
        os.popen(CommandConst.XCode.BOOT_DEVICE % {'uuid': udid})
        # start device
        logger.info(f'Start the simulator!')
        start_vd = CommandConst.XCode.START_SIMULATOR % {'uuid': udid}
        os.popen(start_vd)
        timer = 0
        while timer <= TimeConst.Timeout.TIMEOUT_60:
            TimeUtil.short_sleep()
            active_devices = os.popen(
                CommandConst.XCode.GET_LIST_DEVICES).read()
            if udid in active_devices:
                return True
            else:
                timer += 5
        return False

    @staticmethod
    def stop(platform: str):
        if platform == DeviceConst.Android.ANDROID:
            command_kill_emulator = GetUtil.suite_get(DeviceConst.OBJ).get(CommandConst.ADB.ADB_PATH) % \
                {'username': GetUtil.suite_get(EnvironmentConst.Environment.ENV_OBJ).active_user} + \
                CommandConst.ADB.KILL_EMULATOR % \
                {'emulator_name': GetUtil.suite_get(
                    DeviceConst.Android.EMULATOR_NAME)}
            os.popen(command_kill_emulator)
            logger.info(f'Stop android emulator!')
        else:
            os.popen(CommandConst.XCode.SHUTDOWN_DEVICE %
                     {'uuid': GetUtil.suite_get(DeviceConst.iOS.UDID)})
            os.popen(CommandConst.XCode.KILL_SIMULATOR)
            logger.info(f'Stop ios simulator!')

    @staticmethod
    def is_device_online():
        platform = os.getenv(AppiumConst.Client.PLATFORM_NAME)
        # if device offline => break flow
        if platform == DeviceConst.Android.ANDROID:
            is_online = CommandConst.ADB.DEVICE_OFFLINE_ERROR not in os.popen(
                GetUtil.suite_get(DeviceConst.OBJ).get(CommandConst.ADB.ADB_PATH) %
                {'username': GetUtil.suite_get(EnvironmentConst.Environment.ENV_OBJ).active_user} +
                CommandConst.ADB.LIST_DEVICES).read()
        elif platform == DeviceConst.iOS.IOS:
            is_online = CommandConst.XCode.ERROR_NO_DEVICE_ONLINE not in os.popen(
                CommandConst.XCode.GET_LIST_DEVICES).read()
        else:
            raise Exception(f'Do not support {platform}!')
        if not is_online:
            raise (
                Exception(f'Device {CommandConst.ADB.DEVICE_OFFLINE_ERROR}'))
        return True

    @staticmethod
    def is_app_installed_on_device(platform: str):
        app_conf = GetUtil.suite_get(
            EnvironmentConst.Environment.CONFIG_APP_OBJ)
        empty_cmd: str = ''
        device_conf = GetUtil.suite_get(DeviceConst.OBJ)
        if platform == DeviceConst.Android.ANDROID:
            active_user = GetUtil.suite_get(
                EnvironmentConst.Environment.ENV_OBJ).active_user
            adb_path = device_conf.get(CommandConst.ADB.ADB_PATH) % {
                'username': active_user}

            is_app_installed = True if os.popen(adb_path + CommandConst.ADB.GET_EXISTED_PACKAGE_APP % (
                GetUtil.suite_get(DeviceConst.Android.EMULATOR_NAME),
                app_conf.get(AppiumConst.Client.APP_PACKAGE))).read() != empty_cmd else False

        else:
            start_vd = CommandConst.XCode.GET_APP_BY_BUNDLE_ID % {'uuid': GetUtil.suite_get(DeviceConst.iOS.UDID),
                                                                  'bundle_id': app_conf.get(DeviceConst.iOS.BUNDLE_IDENTIFIER)}
            is_app_installed = True if app_conf.get(
                DeviceConst.iOS.APP) in os.popen(start_vd).read() else False

        logger.debug(f"Is App installed on devices: {is_app_installed}")
        return is_app_installed

    @staticmethod
    def install_app(platform: str, is_cloud_app: bool = False):
        logger.info('Installing app...')

        device_conf = GetUtil.suite_get(DeviceConst.OBJ)
        if platform == DeviceConst.Android.ANDROID:
            active_user = GetUtil.suite_get(
                EnvironmentConst.Environment.ENV_OBJ).active_user
            adb_path = device_conf.get(CommandConst.ADB.ADB_PATH) % {
                'username': active_user}

            cmd = os.popen(adb_path + CommandConst.ADB.INSTALL_APP % (GetUtil.suite_get(DeviceConst.Android.EMULATOR_NAME),
                                                                      VirtualDeviceUtil.get_app_path(platform, is_cloud_app))).read()
        else:
            start_vd = CommandConst.XCode.INSTALL_APP % {'uuid': GetUtil.suite_get(DeviceConst.iOS.UDID),
                                                         'app_path': VirtualDeviceUtil.get_app_path(platform, is_cloud_app)}
            logger.info(f'Installing app with {start_vd}')
            cmd = os.popen(start_vd).read()

        if CommandConst.ADB.FILE_NOT_FOUND_ERROR[0] == cmd or CommandConst.ADB.FILE_NOT_FOUND_ERROR[1] in cmd:
            raise (Exception(cmd))
        else:
            if VirtualDeviceUtil.waiting_to_process_app_complete(platform, is_install_method=True):
                logger.info(f"Installed  {platform} App.")
            else:
                logger.info(f"Installed  {platform} App In-Complete.")

    @staticmethod
    def remove_app(platform: str):
        logger.info('Removing app...')

        app_conf = GetUtil.suite_get(
            EnvironmentConst.Environment.CONFIG_APP_OBJ)
        device_conf = GetUtil.suite_get(DeviceConst.OBJ)
        if platform == DeviceConst.Android.ANDROID:
            active_user = GetUtil.suite_get(
                EnvironmentConst.Environment.ENV_OBJ).active_user
            adb_path = device_conf.get(CommandConst.ADB.ADB_PATH) % {
                'username': active_user}

            os.popen(adb_path + CommandConst.ADB.REMOVE_APP % (GetUtil.suite_get(DeviceConst.Android.EMULATOR_NAME),
                                                               app_conf.get(AppiumConst.Client.APP_PACKAGE)))
        else:
            start_vd = CommandConst.XCode.UNINSTALL_APP % {'uuid': GetUtil.suite_get(DeviceConst.iOS.UDID),
                                                           'bundle_id': app_conf.get(DeviceConst.iOS.BUNDLE_IDENTIFIER)}
            os.popen(start_vd)
        TimeUtil.short_sleep()
        if VirtualDeviceUtil.waiting_to_process_app_complete(platform, is_install_method=False):
            logger.info(f"Uninstalled  {platform} App.")
        else:
            logger.info(f"Uninstalled  {platform} App In-Complete.")

    @staticmethod
    def waiting_to_process_app_complete(platform: str, is_install_method: bool = True):
        TimeUtil.short_sleep()
        app_conf = GetUtil.suite_get(
            EnvironmentConst.Environment.CONFIG_APP_OBJ)
        empty_cmd: str = ''

        def __is_completed(process_app_complete):
            if platform == DeviceConst.Android.ANDROID and is_install_method:
                return app_conf.get(AppiumConst.Client.APP_PACKAGE) in process_app_complete
            elif platform == DeviceConst.iOS.IOS and is_install_method:
                return app_conf.get(DeviceConst.iOS.APP).lower() in process_app_complete.lower()
            else:
                return True if process_app_complete == empty_cmd else False

        timer = 0
        while timer <= TimeConst.Timeout.TIMEOUT_60:
            if platform == DeviceConst.Android.ANDROID:
                active_user = GetUtil.suite_get(
                    EnvironmentConst.Environment.ENV_OBJ).active_user
                adb_path = GetUtil.suite_get(DeviceConst.OBJ).get(
                    CommandConst.ADB.ADB_PATH) % {'username': active_user}

                process_app_complete = os.popen(adb_path + CommandConst.ADB.GET_EXISTED_PACKAGE_APP % (
                    GetUtil.suite_get(DeviceConst.Android.EMULATOR_NAME),
                    app_conf.get(AppiumConst.Client.APP_PACKAGE))).read()

            else:
                cmd = CommandConst.XCode.GET_APP_BY_BUNDLE_ID % {'uuid': GetUtil.suite_get(DeviceConst.iOS.UDID),
                                                                 'bundle_id': app_conf.get(DeviceConst.iOS.BUNDLE_IDENTIFIER)}
                logger.info(f'Install app completed?\n {cmd}')
                process_app_complete = os.popen(cmd).read()

            if __is_completed(process_app_complete):
                return True
            else:
                timer += 5
        return False

    @staticmethod
    def get_app_path(platform: str, is_cloud_app: bool):
        app_conf = GetUtil.suite_get(
            EnvironmentConst.Environment.CONFIG_APP_OBJ)
        if not is_cloud_app:
            if platform == DeviceConst.Android.ANDROID:
                path = f"{PathUtil.join_prj_root_path(PathConst.INSTALL_ANDROID_APP_PATH)}/{app_conf.get(DeviceConst.Android.APP)}"
            else:
                path = f"{PathUtil.join_prj_root_path(PathConst.INSTALL_IOS_APP_PATH)}/{app_conf.get(DeviceConst.iOS.APP)}"

            if PathUtil.is_path_correct(path):
                return path
            else:
                raise Exception(f'Path {path} is not correct.')
        else:
            # Waiting until app repo TODO
            pass

    @staticmethod
    def get_udid() -> Dict:
        """
        :return: Dictionary {os_version: [{name: device_model, udid: udid_str}]}
        e.g {'15.5': [{'name': 'iPhone 8', 'udid': '6BF8186C-9E62-48CF-AED4-05FD1D38FEF2'},
                        {'name': 'iPhone 8 Plus', 'udid': '46503C11-FF95-4DE1-81E4-8A2BC8B2DA4E'}],

        """
        r = os.popen(CommandConst.XCode.LIST_ALL_SIMULATORS)
        d = {}
        for k, v in JsonConverterUtil.convert_string_to_json(r.read())['devices'].items():
            if DeviceConst.iOS.IOS.lower() in k.lower():
                name = k.split('.')[-1].replace('-', '.').replace('iOS.', '')
                tmp = []
                for i in v:
                    if 'iphone' or 'ipad' in i['name'].lower():
                        tmp.append({'name': i['name'], 'udid': i['udid']})
                d[name] = tmp
        return d

    @staticmethod
    def get_supported_udid(os_version: str, device_model: str) -> str:
        """
        :param os_version: iOS's os version. e.g. 15.5 or 16.0
        :param device_model:  iOS's device model. e.g. Iphone 14 Pro Max
        :return: udid string which is associated to the os and platform name
        """
        if os_version not in DeviceConst.iOS.SUPPORT_VERSION:
            raise Exception(
                f'Not support ios version: {os_version}. Support only: {DeviceConst.iOS.SUPPORT_VERSION}')
        else:
            try:
                for i in VirtualDeviceUtil.get_udid().get(os_version):
                    if i.get('name') == device_model:
                        return i.get('udid')
            except Exception as e:
                raise e

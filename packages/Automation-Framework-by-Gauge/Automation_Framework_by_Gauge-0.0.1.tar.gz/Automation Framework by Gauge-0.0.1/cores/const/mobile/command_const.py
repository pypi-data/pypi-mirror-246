from ..__const import Const


class CommandConst(Const):
    class ADB:
        EMULATOR_PATH = 'EMULATOR_PATH'
        ADB_PATH = 'ADB_PATH'
        # device_name
        START_EMULATOR = ' -avd %(device_name)s -no-snapshot-load'
        LIST_DEVICES = ' devices'
        KILL_EMULATOR = ' -s %(emulator_name)s emu kill'  # emulator_name
        # get app package from list
        GET_EXISTED_PACKAGE_APP = ' -s %s shell pm list packages | grep %s'
        INSTALL_APP = ' -s %s install %s'  # install app to android from data
        REMOVE_APP = ' -s %s uninstall %s'  # uninstall app from android device
        FILE_NOT_FOUND_ERROR = ['Performing Streamed Install',
                                "The operation couldn't be completed. No such file or directory"]
        DEVICE_OFFLINE_ERROR = 'offline'
        CLEAR_APP_DATA = 'adb shell pm clear %(app_package)s'  # single device

    class XCode:
        # udid
        START_SIMULATOR = 'open -a Simulator --args -CurrentDeviceUDID %(uuid)s'
        KILL_SIMULATOR = 'killall Simulator'
        GET_LIST_DEVICES = 'xcrun simctl getenv booted SIMULATOR_UDID'
        INSTALL_APP = 'xcrun simctl install %(uuid)s %(app_path)s'
        UNINSTALL_APP = 'xcrun simctl uninstall %(uuid)s %(bundle_id)s'
        GET_APP_BY_BUNDLE_ID = 'xcrun simctl get_app_container %(uuid)s %(bundle_id)s'
        LIST_ALL_SIMULATORS = 'xcrun simctl list devices --json'
        ERROR_NO_DEVICE_ONLINE = 'No devices are booted'
        SHUTDOWN_DEVICE = 'xcrun simctl shutdown %(uuid)s'
        BOOT_DEVICE = 'xcrun simctl boot %(uuid)s'

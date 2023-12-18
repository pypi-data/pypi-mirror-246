from ..__const import Const


class DeviceConst(Const):
    OBJ = "DEVICE_OBJ"
    IS_CLOUD_APP = "IS_CLOUD_APP"

    class Android:
        ANDROID = "Android"
        SUPPORT_VERSION = ['11.0', '12.0', '13.0']
        HOME = "ANDROID_HOME"
        HOME_PATH = "ANDROID_HOME_PATH"
        APP = "ANDROID_APP"
        EMULATOR_NAME = "EMULATOR_NAME"

    class iOS:
        SUPPORT_VERSION = ['15.0', '15.5', '16.0', '16.2', '16.3']
        IOS = "iOS"
        APP = "APP"
        UDID = "UDID"
        BUNDLE_IDENTIFIER = "BUNDLE_IDENTIFIER"
        SIMULATOR_OBJ = "SIMULATOR_OBJ"

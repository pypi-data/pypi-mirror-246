from ..__const import Const


class AppiumConst(Const):
    class Server:
        OBJ = "Appium"
        REMOTE_PATH = "REMOTE_PATH"
        SERVER = "APPIUM_SERVER"
        SERVICE = "APPIUM_SERVICE"
        SERVER_PORT = "APPIUM_SERVER_PORT"

    class Client:
        PLATFORM_NAME = "PLATFORM_NAME"
        PLATFORM_VERSION = "PLATFORM_VERSION"
        DEVICE_NAME = "DEVICE_NAME"
        APP_PACKAGE = "APP_PACKAGE"
        APP_ACTIVITIES = "APP_ACTIVITIES"
        AUTOMATION_NAME = "AUTOMATION_NAME"

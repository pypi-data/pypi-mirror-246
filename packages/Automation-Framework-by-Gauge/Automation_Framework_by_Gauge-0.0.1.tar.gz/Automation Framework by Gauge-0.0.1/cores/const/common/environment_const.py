from ..__const import Const


class EnvironmentConst(Const):

    class Logger:
        INFO: str = 'INFO'
        DEBUG: str = 'DEBUG'
        WARNING: str = 'WARNING'
        ERROR: str = 'ERROR'

    class Environment:
        BASE_URL: str = 'BASE_URL'
        PROJECT_NAME: str = 'PROJECT_NAME'
        SIT_ENV: str = 'sit'
        UAT_ENV: str = 'uat'
        STAG_ENV: str = 'staging'
        PREPROD_ENV: str = 'preprod'
        PROD_ENV: list = ['PRODUCTION', 'LIVE']
        LOG_LEVEL: str = 'LOG_LEVEL'
        ENV_OBJ: str = 'ENV_OBJ'
        BROWSER: str = 'BROWSER'
        TOKEN: str = 'TOKEN'
        BUILD_NAME: str = 'BUILD_NAME'
        CONFIG_APP_OBJ = 'APP_CONFIG_OBJ'

    class Driver:
        MOBILE_DRIVER: str = 'MOBILE_DRIVER'
        WEB_DRIVER: str = 'WEB_DRIVER'

    class Mobile:
        BUILD_NAME: str = 'BUILD_NAME'
        PLATFORM: str = 'PLATFORM'

    class Configuration:
        IS_API: str = 'IS_API'
        IS_WEB: str = 'IS_WEB'
        IS_IOS: str = 'IS_IOS'
        IS_ANDROID: str = 'IS_ANDROID'
        IS_E2E: str = 'IS_E2E'
        IS_TEST_LINK: str = 'IS_TEST_LINK'
        IS_HEADLESS: str = 'IS_HEADLESS'
        CONFIG_APP_OBJ = 'APP_CONFIG_OBJ'
        CONFIG_OBJ = 'CONFIG_OBJECT'
        MOBILE_DRIVER = 'MOBILE_DRIVER'
        WEB_DRIVER = 'WEB_DRIVER'

    class Database:
        DB_NAME: str = 'DB_NAME'
        DB_HOST: str = 'DB_HOST'
        DB_USERNAME: str = 'DB_USERNAME'
        DB_PWD: str = 'DB_USERNAME'
        DB_PORT: int = 0
        DB_OBJ: str = 'DB_OBJ'
        MYSQL = 'MYSQL'
        POSTGRES = 'POSTGRES'
        REDIS = 'REDIS'
        MONGODB = 'MONGODB'

    class ConfigPath:
        DB_CONFIG = 'configurations/db.ini'
        TESTLINK_CONFIG = 'configurations/testlink.ini'
        ANDROID_APP_UNDER_TEST = 'configurations/android/{}.ini'
        IOS_APP_UNDER_TEST = 'configurations/ios/{}.ini'
        APPIUM_CONFIG_PATH = 'configurations/mobile/appium/Appium.ini'
        APP_CONFIG_PATH = 'configurations/mobile/app/%(name)s.ini'
        DEVICE_CONFIG_PATH = 'configurations/mobile/device/%(name)s.ini'

    class Driver:
        DRIVER = 'DRIVER'
        MOBILE_DRIVER = ''

    class Swagger:
        SWAGGER_URL = 'SWAGGER_URL'
        SWAGGER_OBJ = 'SWAGGER_OBJ'

    class Testlink:
        NAME = 'TESTLINK'
        TESTLINK_API_URL = 'TESTLINK_API_URL'
        TESTLINK_API_KEY = 'TESTLINK_API_KEY'
        TL_PROJECT_NAME: str = 'TL_PROJECT_NAME'
        TL_TEST_PLAN_NAME: str = 'TL_TEST_PLAN_NAME'

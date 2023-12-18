from ..__const import Const


class PathConst(Const):
    # CONFIGS
    APPIUM_CONFIG_PATH = 'Appium.ini'
    APP_CONFIG_PATH = '%(name)s.ini'
    DEVICE_CONFIG_PATH = '%(name)s.ini'
    DB_CONFIG_PATH = 'configurations/db.ini'

    # ROOT
    PROFILE_PATH = '.profile/automation'
    PROFILE_ROOT = '.profile'

    # UNITTEST

    # Documents
    INSTALL_ANDROID_APP_PATH = 'data/apps/android'
    INSTALL_IOS_APP_PATH = 'data/apps/ios'
    FILE_UPLOAD_PATH = 'data/%(name)s'
    UPLOAD_IMAGES_FILE_PATH = 'data/image/%(name)s'
    UPLOAD_AUDIO_FILE_PATH = 'data/audio/%(name)s'
    UPLOAD_FILES_PATH = 'data/doc/%(name)s'

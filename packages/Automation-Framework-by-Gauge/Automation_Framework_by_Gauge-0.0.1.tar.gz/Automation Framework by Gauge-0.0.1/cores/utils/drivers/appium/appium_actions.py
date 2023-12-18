from cores.utils.drivers.selenium.selenium_base import SeleniumBase


class AppiumActions(SeleniumBase):

    def __init__(self, driver):
        self.__driver = driver
        super().__init__(driver)

    """ Mobile """

    def copy_value_to_clipboard(self, value):
        self.__driver.set_clipboard_text(value)

    def get_data_from_clipboard(self):
        return self.__driver.get_clipboard_text()

    def tap(self, x, y):
        # TODO: I will replace tap of TouchAction with tap of ActionHelpers
        self.touch_action(self.__driver).tap(x=x,
                                             y=y).perform()  # tap of TouchAction

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 0):
        self.__driver.swipe(start_x=start_x,
                            start_y=start_y,
                            end_x=end_x,
                            end_y=end_y,
                            duration=duration)

    def get_screen_mobile_size(self):
        """
        return device_size['width'] and  device_size['height']
        """
        device_size = self.__driver.get_window_size()
        return device_size['width'], device_size['height']

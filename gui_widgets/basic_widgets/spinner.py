#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.Spinner

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class Spinner(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, spinner=None, alert_accept=True, **kwargs):
        super(Spinner, self).__init__(parent, spinner, alert_accept, **kwargs)
        self.__spinner = self._element

    def __getattr__(self, item):
        return getattr(self.__spinner, item, None)

    @property
    def text(self):
        return self.__spinner.text

    def tap(self):
        self.__spinner.click()


class SpinnerList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(SpinnerList, self).__init__(parent, alert_accept, **kwargs)
        self.__spinner_list = self._element_list



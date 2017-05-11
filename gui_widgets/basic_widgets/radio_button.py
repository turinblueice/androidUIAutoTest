#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.RadioButton

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class RadioButton(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, radio_button=None, alert_accept=True, **kwargs):
        super(RadioButton, self).__init__(parent, radio_button, alert_accept, **kwargs)
        self.__radio_button = self._element

    def __getattr__(self, item):

        return getattr(self.__radio_button, item, None)

    def tap(self):
        self.__radio_button.click()


class RadioButtonList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(RadioButtonList, self).__init__(parent, alert_accept, **kwargs)
        self.__radio_button_list = self._element_list



#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.ImageButton

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class ImageButton(mobile_base_element.BaseMobileElement):
    """

    Attribute:
        __image_button:private.
    """
    def __init__(self, parent, image_button=None, alert_accept=True, **kwargs):
        super(ImageButton, self).__init__(parent, image_button, alert_accept, **kwargs)
        self.__image_button = self._element

    def __getattr__(self, item):

        return getattr(self.__image_button, item, None) or super(ImageButton, self).__getattr__(item)

    def tap(self):
        self.__image_button.click()


class ImageButtonList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ImageButtonList, self).__init__(parent, alert_accept, **kwargs)
        self.__image_button_list = self._element_list



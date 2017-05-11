#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.CheckBox

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement

from gui_widgets.basic_widgets import mobile_base_element


class CheckBox(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, check_box=None, alert_accept=True, **kwargs):
        super(CheckBox, self).__init__(parent, check_box, alert_accept, **kwargs)
        self.__check_box = self._element

    def __getattr__(self, item):

        return getattr(self.__check_box, item, None)

    def check(self):
        self.__check_box.click()


class CheckBoxList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(CheckBoxList, self).__init__(parent, alert_accept, **kwargs)
        self.__check_box_list = self._element_list

    @property
    def check_box_list(self):

        return [CheckBox(check_box.parent, check_box) for check_box in self.__check_box_list]


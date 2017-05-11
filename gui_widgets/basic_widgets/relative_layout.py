#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.RelativeLayout

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class RelativeLayout(mobile_base_element.BaseMobileElement):
    """
    Attribute:
        __switch:
    """
    def __init__(self, parent, relative_layout=None, alert_accept=True, **kwargs):
        super(RelativeLayout, self).__init__(parent, relative_layout, alert_accept, **kwargs)
        self.__relative_layout = self._element

    def __getattr__(self, item):
        return getattr(self.__relative_layout, item, None)

    def tap(self):
        self.__relative_layout.click()

    def get_webelement(self):
        return self.__relative_layout


class RelativeLayoutList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(RelativeLayoutList, self).__init__(parent, alert_accept, **kwargs)
        self.__relative_layout_list = self._element_list

    @property
    def relative_layout_list(self):
        if self.__relative_layout_list:
            return [RelativeLayout(layout.parent, layout) for layout in self.__relative_layout_list]
        return None



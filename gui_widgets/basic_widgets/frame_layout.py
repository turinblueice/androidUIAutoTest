#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.FrameLayout

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class FrameLayout(mobile_base_element.BaseMobileElement):
    """
    Attribute:

    """
    def __init__(self, parent, frame_layout=None, alert_accept=True, **kwargs):
        super(FrameLayout, self).__init__(parent, frame_layout, alert_accept, **kwargs)
        self.__frame_layout = self._element
        self._scroll_view = self.__frame_layout

    def __getattr__(self, item):
        return getattr(self.__frame_layout, item, None)

    def tap(self):
        self.__frame_layout.click()


class FrameLayoutList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(FrameLayoutList, self).__init__(parent, alert_accept, **kwargs)
        self.__frame_layout_list = self._element_list

    @property
    def frame_list(self):

        if self.__frame_layout_list:
            return [FrameLayout(item.parent, item) for item in self.__frame_layout_list]
        return None



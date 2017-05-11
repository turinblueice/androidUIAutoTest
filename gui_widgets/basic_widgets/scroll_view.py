#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:android.widget.ScrollView

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class ScrollView(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, scroll_view=None, alert_accept=True, **kwargs):
        super(ScrollView, self).__init__(parent, scroll_view, alert_accept, **kwargs)
        self.__scroll_view = self._element

    def __getattr__(self, item):

        return getattr(self.__scroll_view, item, None)

    def tap(self):
        self.__scroll_view.click()


class ScrollViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ScrollViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__scroll_view_list = self._element_list

    @property
    def scroll_view_list(self):
        if self.__scroll_view_list:
            return [ScrollView(layout.parent, layout) for layout in self.__scroll_view_list]
        return None


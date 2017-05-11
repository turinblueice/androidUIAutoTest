#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:android.widget.TabWidget

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class TabWidget(mobile_base_element.BaseMobileElement):
    """
        Summary:
            tabwidget类
    """
    def __init__(self, parent, tab=None, alert_accept=True, **kwargs):
        super(TabWidget, self).__init__(parent, tab, alert_accept, **kwargs)
        self.__tab = self._element

    def __getattr__(self, item):
        return getattr(self.__tab, item, None)

    @property
    def text(self):
        return self.__tab.text

    def tap(self):
        self.__tab.click()


class TabList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(TabList, self).__init__(parent, alert_accept, **kwargs)
        self.__tab_list = self._element_list

    @property
    def tab_widget_list(self):
        if self.__tab_list:
            return [TabWidget(tab_item.parent, tab_item) for tab_item in self.__tab_list]
        return None



#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.support.v4.view.ViewPager

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class ViewPager(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, view=None, alert_accept=True, **kwargs):
        super(ViewPager, self).__init__(parent, view, alert_accept, **kwargs)
        self._layout_view = self._element

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    def tap(self, wait_time=0.5):
        self._layout_view.click()
        # 显示等待wait_Time秒
        self.base_parent.implicitly_wait(wait_time)


class ViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__layout_view_list = self._element_list

    @property
    def pager_view_list(self):
        if self.__layout_view_list:
            return [ViewList(item.parent, item) for item in self.__layout_view_list]
        return None


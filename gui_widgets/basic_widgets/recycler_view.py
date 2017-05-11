#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.ListView
Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
import time
from gui_widgets.basic_widgets import mobile_base_element


class RecyclerView(mobile_base_element.BaseMobileElement):
    """

    Attribute:

    """
    def __init__(self, parent, recycler_view=None, alert_accept=True, **kwargs):
        super(RecyclerView, self).__init__(parent, recycler_view, alert_accept, **kwargs)
        self.__recycler_view = self._element
        self._scroll_view = self.__recycler_view

    def __getattr__(self, item):
        return getattr(self.__recycler_view, item, None)

    def tap(self):
        self.__recycler_view.click()

    def swipe_right_entire_recycler_view(self):
        """
            Summary:
                向右滑动整个view宽度

        """
        location = self.__recycler_view.location
        size = self.__recycler_view.size
        y = location['y'] + size['height'] / 2
        start_x = location['x'] + 1
        end_x = location['x'] + size['width'] - 1

        self.swipe_right(y, start_x, end_x)
        time.sleep(2)

    def swipe_left_entire_recycler_view(self):
        """
            Summary:
                向左滑动整个view宽度

        """
        location = self.__recycler_view.location
        size = self.__recycler_view.size
        y = location['y'] + size['height'] / 2
        end_x = location['x'] + 1
        start_x = location['x'] + size['width'] - 1

        self.swipe_left(y, start_x, end_x)
        time.sleep(2)


class RecyclerViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(RecyclerViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__recycler_view_list = self._element_list

    @property
    def recycler_list(self):

        if self.__recycler_view_list:
            return [RecyclerView(item.parent, item) for item in self.__recycler_view_list]
        return None


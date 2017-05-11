#-*-coding:utf8-*-

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


class ListView(mobile_base_element.BaseMobileElement):
    """

    Attribute:
        __image_button:private.
    """
    def __init__(self, parent, list_view=None, alert_accept=True, **kwargs):
        super(ListView, self).__init__(parent, list_view, alert_accept, **kwargs)
        self.__list_view = self._element

    def __getattr__(self, item):
        return getattr(self.__list_view, item, None)

    def tap(self):
        self.__list_view.click()

    def swipe_up_entire_list_view(self):
        """
            Summary:
                向上滑动整个列表的高度

        """
        location = self.__list_view.location
        size = self.__list_view.size
        x = location['x'] + size['width'] / 2
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        self.swipe_up(x, start_y, end_y)
        time.sleep(2)

    def swipe_down_entire_list_view(self):
        """
            Summary:
                向下滑动整个列表的高度
        """
        location = self.__list_view.location
        size = self.__list_view.size
        x = location['x'] + size['width'] / 2
        end_y = location['y'] + size['height'] - 1
        start_y = location['y'] + 1

        self.swipe_up(x, start_y, end_y)
        time.sleep(2)


class ListViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ListViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__list_view_list = self._element_list



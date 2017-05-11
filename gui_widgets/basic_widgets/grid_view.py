#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:android.widget.GridView

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class GridView(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, grid_view=None, alert_accept=True, **kwargs):
        super(GridView, self).__init__(parent, grid_view, alert_accept, **kwargs)
        self.__grid_view = self._element

    def __getattr__(self, item):

        return getattr(self.__grid_view, item, None)

    def tap(self):
        self.__grid_view.click()


class GridViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(GridViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__grid_view_list = self._element_list

    @property
    def grid_view_list(self):
        if self.__grid_view_list:
            return [GridView(layout.parent, layout) for layout in self.__grid_view_list]
        return None


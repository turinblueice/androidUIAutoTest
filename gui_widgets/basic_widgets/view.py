#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.view.View

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class View(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, view=None, alert_accept=True, **kwargs):
        super(View, self).__init__(parent, view, alert_accept, **kwargs)
        self.__view = self._element

    def __getattr__(self, item):
        return getattr(self.__view, item, None)

    @property
    def text(self):
        if isinstance(self.__view.text, unicode):
            return self.__view.text.encode('utf8')
        return self.__view.text

    def tap(self, wait_time=0.5):
        self.__view.click()
        # 显示等待wait_Time秒
        self.base_parent.implicitly_wait(wait_time)

    def clear_text_field(self):
        self.__view.clear()  #Clears the text if it’s a text entry element.

    def send_keys(self, *values):
        self.__view.send_keys(*values)
        # 显示等待0.5秒
        self.base_parent.implicitly_wait(0.5)


class ViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__view_list = self._element_list

    @property
    def view_list(self):

        if self.__view_list:
            return [View(item.parent, item) for item in self.__view_list]



#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.Button

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement

from gui_widgets.basic_widgets import mobile_base_element


class Button(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, button=None, alert_accept=True, **kwargs):
        super(Button, self).__init__(parent, button, alert_accept, **kwargs)
        self.__button = self._element

    def __getattr__(self, item):
        return getattr(self.__button, item, None)

    def tap(self, timeout=0.5):
        """
        :param timeout 等待时间
        Args:
            
        Returns:
        Raises
        """
        self.__button.click()
        self.base_parent.implicitly_wait(timeout)


class ButtonList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ButtonList, self).__init__(parent, alert_accept, **kwargs)
        self.__button_list = self._element_list

    @property
    def button_list(self):

        return [Button(button.parent, button) for button in self.__button_list]



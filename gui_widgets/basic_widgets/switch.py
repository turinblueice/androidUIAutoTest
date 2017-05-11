#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.Switch

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class Switch(mobile_base_element.BaseMobileElement):
    """
    Attribute:
        __switch:
    """
    def __init__(self, parent, switch=None, alert_accept=True, **kwargs):
        super(Switch, self).__init__(parent, switch, alert_accept, **kwargs)
        self.__switch = self._element

    def __getattr__(self, item):

        return getattr(self.__switch, item, None)

    def tap(self):
        self.__switch.click()

    def is_selected(self):

        status = self.__switch.get_attribute('checked')
        if status == 'true':
            return True
        else:
            return False


class SwitchList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(SwitchList, self).__init__(parent, alert_accept, **kwargs)
        self.__switch_list = self._element_list

    @property
    def switch_list(self):
        if self.__switch_list:
            return [Switch(switch_item.parent, switch_item) for switch_item in self.__switch_list]
        return None



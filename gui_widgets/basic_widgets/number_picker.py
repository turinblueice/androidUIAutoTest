#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.ImageView

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class NumberPicker(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, view=None, alert_accept=True, **kwargs):
        super(NumberPicker, self).__init__(parent, view, alert_accept, **kwargs)
        self._view = self._element

    def __getattr__(self, item):
        return getattr(self._view, item, None)

    @property
    def view_element(self):
        return self._view

    def tap(self):
        self._view.click()


class NumberPickerList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(NumberPickerList, self).__init__(parent, alert_accept, **kwargs)
        self._number_picker_list = self._element_list

    @property
    def item_list(self):
        if self._number_picker_list:
            return [NumberPicker(item.parent, item) for item in self._number_picker_list]
        return None



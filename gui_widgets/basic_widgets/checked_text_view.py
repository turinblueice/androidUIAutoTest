#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.CheckBox

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from base import base_frame_view
from appium.webdriver.webelement import WebElement
from gui_widgets.basic_widgets import mobile_base_element


class CheckedTextView(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, checked_text_view=None, alert_accept=True, **kwargs):
        super(CheckedTextView, self).__init__(parent, checked_text_view, alert_accept, **kwargs)
        self.__checked_text_view = self._element

    def __getattr__(self, item):

        return getattr(self.__checked_text_view, item, None)

    def tap(self):
        self.__checked_text_view.click()

    def is_selected(self):

        status = self.__checked_text_view.get_attribute('checked')
        if status == 'true':
            return True
        else:
            return False


class CheckedTextViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(CheckedTextViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__check_text_view_list = self._element_list

    @property
    def checked_text_view_list(self):

        return [CheckedTextView(check_box.parent, check_box) for check_box in self.__check_text_view_list]


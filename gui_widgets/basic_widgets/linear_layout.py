#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.LinearLayout

Authors: Turinblueice
Date:    16/3/15 16:12
"""


from gui_widgets.basic_widgets import mobile_base_element
import time


class LinearLayout(mobile_base_element.BaseMobileElement):
    """
    Attribute:
        __switch:
    """
    def __init__(self, parent, linear_layout=None, alert_accept=True, **kwargs):
        super(LinearLayout, self).__init__(parent, linear_layout, alert_accept, **kwargs)
        self.__linear_layout = self._element

    def __getattr__(self, item):
        return getattr(self.__linear_layout, item, None)

    def tap(self, timeout=3):
        self.__linear_layout.click()
        time.sleep(timeout)


class LinearLayoutList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(LinearLayoutList, self).__init__(parent, alert_accept, **kwargs)
        self.__linear_layout_list = self._element_list

    @property
    def layout_list(self):

        return [LinearLayout(layout.parent, layout) for layout in self.__linear_layout_list]



#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:android.widget.TextView

Authors: Turinblueice
Date:    16/3/15 16:12
"""

from gui_widgets.basic_widgets import mobile_base_element
import time

class TextView(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, text_view=None, alert_accept=True, **kwargs):
        super(TextView, self).__init__(parent, text_view, alert_accept, **kwargs)
        self.__text_view = self._element

    def __getattr__(self, item):

        return getattr(self.__text_view, item, None)

    @property
    def text(self):

        if isinstance(self.__text_view.text, unicode):
            return self.__text_view.text.encode('utf8')
        return self.__text_view.text

    def tap(self, wait_time=3):
        self.__text_view.click()
        time.sleep(wait_time)


class TextViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(TextViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__text_view_list = self._element_list

    @property
    def text_view_list(self):
        if self.__text_view_list:
            return [TextView(layout.parent, layout) for layout in self.__text_view_list]
        return None


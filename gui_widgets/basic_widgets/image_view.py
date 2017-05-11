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

from gui_widgets.basic_widgets import mobile_base_element
import time


class ImageView(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, image_view=None, alert_accept=True, **kwargs):
        super(ImageView, self).__init__(parent, image_view, alert_accept, **kwargs)
        self.__image_view = self._element

    def __getattr__(self, item):
        return getattr(self.__image_view, item, None)

    def tap(self, timeout=3):
        self.__image_view.click()
        time.sleep(timeout)


class ImageViewList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(ImageViewList, self).__init__(parent, alert_accept, **kwargs)
        self.__image_view_list = self._element_list

    @property
    def image_list(self):

        if self.__image_view_list:
            return [ImageView(item.parent, item) for item in self.__image_view_list]
        return None



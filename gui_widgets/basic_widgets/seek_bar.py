#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:class:android.widget.SeekBar

Authors: Turinblueice
Date:    16/3/16 12:12
"""

from gui_widgets.basic_widgets import mobile_base_element
from util import log

import time


class SeekBar(mobile_base_element.BaseMobileElement):
    """

    """
    def __init__(self, parent, seekbar=None, alert_accept=True, **kwargs):
        super(SeekBar, self).__init__(parent, seekbar, alert_accept, **kwargs)
        self.__seekbar = self._element

    def __getattr__(self, item):
        return getattr(self.__seekbar, item, None)

    def tap(self, timeout=0.5):
        """
        :param timeout 等待时间
        Args:
            
        Returns:
        Raises
        """
        self.__seekbar.click()
        self.base_parent.implicitly_wait(timeout)

    @property
    def rectangle(self):
        """
            Summary:
                矩形框
        Returns:

        """
        left_top_x = self.__seekbar.location['x']
        left_top_y = self.__seekbar.location['y']
        width = self.__seekbar.size['width']
        height = self.__seekbar.size['height']

        return [(left_top_x, left_top_y), (width, height)]

    def slide(self, direction='left', slide_ratio=0.5, start_location=None, end_location=None):
        """
            Summary:
                滑动
        Args:
            start_location: 开始地址(x,y)
            end_location: 结束地址(x,y)
            direction: 'left' or 'right'
            slide_ratio: 滑动长度的比率

        Returns:

        """
        if isinstance(start_location, (tuple, list)) and isinstance(end_location, (tuple, list)):
            self.base_parent.swipe(start_location[0], start_location[1], end_location[0], end_location[1])
        else:
            if direction not in ('left', 'right') or slide_ratio > 1 or slide_ratio <= 0:
                log.logger.error("direction不等于left或right,或者slide_ratio不在0~1的范围内")
                raise

            if direction == 'left':
                log.logger.info("向左滑动")

                # 向左滑动,默认起始点为滑块最右端
                start_location = (self.__seekbar.location['x']+self.__seekbar.size['width']-1,
                                  self.__seekbar.location['y']+self.__seekbar.size['height']/2)
                end_location = (self.__seekbar.location['x']+self.__seekbar.size['width']*(1-slide_ratio),
                                self.__seekbar.location['y']+self.__seekbar.size['height']/2)
                self.base_parent.swipe(start_location[0], start_location[1], end_location[0], end_location[1])

            elif direction == 'right':
                # 向右滑动,默认起始点为滑块最左端

                log.logger.info("向右滑动")
                start_location = (self.__seekbar.location['x'] + 1,
                                  self.__seekbar.location['y'] + self.__seekbar.size['height'] / 2)
                end_location = (self.__seekbar.location['x'] + self.__seekbar.size['width'] * slide_ratio,
                                self.__seekbar.location['y'] + self.__seekbar.size['height'] / 2)
                self.base_parent.swipe(start_location[0], start_location[1], end_location[0], end_location[1])
            log.logger.info('滑动完毕')
            time.sleep(3)


class SeekBarList(mobile_base_element.BaseMobileElementList):
    """

    """
    def __init__(self, parent, alert_accept=True, **kwargs):
        super(SeekBarList, self).__init__(parent, alert_accept, **kwargs)
        self.__seekbar_list = self._element_list

    @property
    def seekbar_list(self):

        return [SeekBar(seekbar.parent, seekbar) for seekbar in self.__seekbar_list]



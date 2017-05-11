# -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法:时间设置messagebox

Authors: Turinblueice
Date:    16/5/03 16:23
"""

import time

from base import base_frame_view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import number_picker
from gui_widgets.basic_widgets import text_view
from util import log


class TimeSettingBox(base_frame_view.BaseFrameView):

    """
        时间设置对话框

    Attributes:

    """

    def __init__(self, parent):
        super(TimeSettingBox, self).__init__(parent)

        self.__layout_frame = linear_layout.LinearLayout(
            self.parent, id='com.qima.kdt:id/parentPanel')

    @property
    def time_alert_title(self):
        """
            Summary:
                左上角时间显示
        """
        id_ = 'com.qima.kdt:id/alertTitle'
        return text_view.TextView(self.base_parent, id=id_)


    @property
    def year_set(self):
        """
            Summary:
                时间设置
        """
        date_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/date_picker')
        pickers = TimeSetItemList(date_picker_layout, type='android.widget.NumberPicker').item_list
        return TimeSetItem(copy=pickers[0], name='年份')

    @property
    def month_set(self):
        """
            Summary:
                时间设置
        """
        date_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/date_picker')
        pickers = TimeSetItemList(date_picker_layout, type='android.widget.NumberPicker').item_list
        return TimeSetItem(copy=pickers[1], name='月份')

    @property
    def day_set(self):
        """
            Summary:
                时间设置
        """
        date_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/date_picker')
        pickers = TimeSetItemList(date_picker_layout, type='android.widget.NumberPicker').item_list
        return TimeSetItem(copy=pickers[2], name='日期')

    @property
    def hour_set(self):
        """
            Summary:
                时间设置
        """
        time_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/time_picker')
        pickers = TimeSetItemList(time_picker_layout, type='android.widget.NumberPicker').item_list
        return TimeSetItem(copy=pickers[0], name='小时')

    @property
    def minute_set(self):
        """
            Summary:
                时间设置
        """
        time_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/time_picker')
        pickers = TimeSetItemList(time_picker_layout, type='android.widget.NumberPicker').item_list
        return TimeSetItem(copy=pickers[1], name='分钟')

    @property
    def second_set(self):
        """
            Summary:
                时间设置
        """
        time_picker_layout = linear_layout.LinearLayout(self.__layout_frame, id='com.qima.kdt:id/time_picker')
        pickers = TimeSetItemList(time_picker_layout, type='android.widget.NumberPicker').item_list
        if len(pickers) == 3:
            return TimeSetItem(copy=pickers[2], name='秒钟')
        return None

    @property
    def ok_button(self):
        """
            Summary:
                确认按钮
        """
        id_ = 'android:id/button1'
        return button.Button(self.__layout_frame, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = 'android:id/button2'
        return button.Button(self.__layout_frame, id=id_)

    def tap_ok_button(self):
        """
            Summary:
                点击确认按钮
        """
        log.logger.info("开始点击确认按钮")
        self.ok_button.tap()
        log.logger.info("完成点击")
        time.sleep(2)

    def tap_cancel_button(self):
        """
            Summary:
                点击删除按钮
        """
        log.logger.info("开始点击删除按钮")
        self.cancel_button.tap()
        log.logger.info("完成点击")
        time.sleep(2)


class TimeSetItem(number_picker.NumberPicker):
    """
        Summary:
            时间编辑模块
    """
    def __init__(self, parent=None, item=None, copy=None, name=None, **kwargs):
        if not copy:
            super(TimeSetItem, self).__init__(parent, item, **kwargs)
        else:
            super(TimeSetItem, self).__init__(copy.parent, copy.view_element, **kwargs)
            self._name = name
        self.__goods_TimeSet_item = self._view

    def __getattr__(self, item):
        return getattr(self.__goods_TimeSet_item, item, None)

    @property
    def middle_set_edit(self):

        """
            Summary:
                NumberPicker 元素的中间编辑框
        """
        id_ = 'android:id/numberpicker_input'
        return edit_text.EditText(self.__goods_TimeSet_item, id=id_)

    @property
    def top_time_button(self):
        """
            Summary:
                NumberPicker 元素的顶部时间按钮
        """
        type_ = "android.widget.Button"
        elems = button.ButtonList(self.__goods_TimeSet_item, type=type_).button_list
        if len(elems) > 1:
            return elems[0]  # 有时候上边时间按钮不显示
        return None

    @property
    def bottom_time_button(self):
        """
            Summary:
                NumberPicker 元素的底部时间按钮
        """
        type_ = "android.widget.Button"
        elems = button.ButtonList(self.__goods_TimeSet_item, type=type_).button_list
        if len(elems) > 1:
            return elems[1]  # 有时候上边时间按钮不显示
        return elems[0]

    def input_time_value(self, num):
        """
            Summary:
                输入时间值
        """
        log.logger.info("开始清空{}输入框".format(self._name))
        self.middle_set_edit.clear_text_field()
        log.logger.info("开始输入{}值".format(self._name))
        self.middle_set_edit.send_keys(num)
        log.logger.info("完成输入")
        time.sleep(2)

    def swipe_down_one_time_cell(self):
        """
            Summary:
                向下滑动一个时间点
        """
        middle_cell_location = self.middle_set_edit.location
        middle_cell_size = self.middle_set_edit.size

        x = middle_cell_location['x'] + middle_cell_size['width']/2
        start_y = middle_cell_location['y'] - middle_cell_size['width']/4
        end_y = middle_cell_location['y'] + middle_cell_size['width']*1.1
        log.logger.info("开始向下滑动{}控件".format(self._name))
        self.swipe_down(x, start_y, end_y)
        log.logger.info("滑动完毕")
        time.sleep(1)

    def swipe_up_one_time_cell(self):
        """
            Summary:
                向上滑动一个时间点
        """
        middle_cell_location = self.middle_set_edit.location
        middle_cell_size = self.middle_set_edit.size

        x = middle_cell_location['x'] + middle_cell_size['width'] / 2
        end_y = middle_cell_location['y'] - middle_cell_size['width']/4
        start_y = middle_cell_location['y'] + middle_cell_size['width']*1.1
        log.logger.info("开始向上滑动{}控件".format(self._name))
        self.swipe_up(x, start_y, end_y)
        log.logger.info("滑动完毕")
        time.sleep(1)


class TimeSetItemList(number_picker.NumberPickerList):

    def __init__(self, parent, **kwargs):
        super(TimeSetItemList, self).__init__(parent, **kwargs)
        self.__item_list = self._number_picker_list

    @property
    def item_list(self):

        if self.__item_list:
            return [TimeSetItem(item.parent, item) for item in self.__item_list]
        return None

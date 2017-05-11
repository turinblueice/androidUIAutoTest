#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:自定义贴纸对话框
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import image_view

from activities import activities

import time


class CustomPasterMsgBox(base_frame_view.BaseFrameView):
    """
        Summary:
            自定义贴纸对话框
    """

    def __init__(self, parent):
        super(CustomPasterMsgBox, self).__init__(parent)
        self._layout_view = frame_layout.FrameLayout(self.parent, type='android.widget.FrameLayout')

    def __getattr__(self, item):

        return getattr(self._layout_view, item) or getattr(self.base_parent, item)

    @property
    def title(self):
        """
            Summary:
                对话框的标题
        """
        id_ = 'com.jiuyan.infashion:id/tv_dialog_sticker_name'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def use_immediate_button(self):
        """
            Summary:
                立即使用按钮
        """
        id_ = 'com.jiuyan.infashion:id/circularButtonUse'
        return button.Button(self._layout_view, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = 'com.jiuyan.infashion:id/btn_dismiss'
        return image_view.ImageView(self._layout_view, id=id_)

    # **************************操作方法****************************

    def tap_use_button(self):
        """
            Summary:
                点击立即使用按钮
        :return:
        """
        log.logger.info("开始点击立即使用按钮")
        self.use_immediate_button.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.CAMERA2, 10):
            log.logger.info("成功进入拍照页")
            return True
        log.logger.error("进入拍照失败")
        return False

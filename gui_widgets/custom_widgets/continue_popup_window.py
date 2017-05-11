#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:"是否继续上次临时保存编辑"提示框
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from activities import activities

import time


class ContinuePopupWindow(base_frame_view.BaseFrameView):
    """
        Summary:
            底部弹出框,临时保存/不保存/取消
    """

    def __init__(self, parent, **kwargs):
        super(ContinuePopupWindow, self).__init__(parent)
        if kwargs:
            self._layout_view = self.find_element(**kwargs)
        else:
            self._layout_view = self.find_element(id='android:id/content')

    def __getattr__(self, item):

        if hasattr(self._linear_layout, item):
            return getattr(self._linear_layout, item)
        return getattr(self.base_parent, item)

    @property
    def new_button(self):
        """
            Summary:
                新建按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_publish_menu_commen_msg_cancel'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def continue_button(self):
        """
            Summary:
                继续按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_publish_menu_commen_msg_confirm'
        return text_view.TextView(self._layout_view, id=id_)

    # ***********************************操作方法**************************

    def tap_new_button(self):
        """
            Summary:
                点击新建按钮
        Returns:

        """
        log.logger.info("开始点击新建按钮")
        self.new_button.tap()
        log.logger.info("点击完毕")
        time.sleep(3)

    def tap_continue_button(self):
        """
            Summary:
                点击继续按钮
        Returns:

        """
        log.logger.info("开始点击继续按钮")
        self.continue_button.tap()
        log.logger.info("点击完毕")
        if self.base_parent.wait_activity(activities.ActivityNames.PUBLISH_CORE, 10):
            log.logger.info('成功进入发布加工页')
            return True
        log.logger.error("进入发布加工页失败")
        return False

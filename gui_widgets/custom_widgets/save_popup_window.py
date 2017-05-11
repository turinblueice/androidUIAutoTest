#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:照片临时保存/不保存提示框
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from activities import activities

import time


class SavePopupWindow(base_frame_view.BaseFrameView):
    """
        Summary:
            底部弹出框,临时保存/不保存/取消
    """

    def __init__(self, parent, **kwargs):
        super(SavePopupWindow, self).__init__(parent)
        if kwargs:
            self._layout_view = self.find_element(**kwargs)
        else:
            self._layout_view = self.find_element(id='android:id/content')

    def __getattr__(self, item):

        if hasattr(self._linear_layout, item):
            return getattr(self._linear_layout, item)
        return getattr(self.base_parent, item)

    @property
    def save_temporary_button(self):
        """
            Summary:
                临时保存按钮
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_confirm'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def no_save_button(self):
        """
            Summary:
                不保存按钮
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_negative'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                对话框上的取消/拒绝按钮
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_cancel'
        return text_view.TextView(self._layout_view, id=id_)

    # ***********************************操作方法**************************

    def tap_save_temporary_button(self):
        """
            Summary:
                点击临时保存按钮
        Returns:

        """
        log.logger.info("开始点击临时保存页")
        self.save_temporary_button.tap()
        log.logger.info("点击完毕")
        if self.base_parent.wait_activity(activities.ActivityNames.PHOTO_PICKER, 10):
            log.logger.info('成功进入图片选择页')
            return True
        log.logger.error("进入图片选择按钮失败")
        return False

    def tap_no_save_button(self):
        """
            Summary:
                点击不保存按钮
        Returns:

        """
        log.logger.info("开始点击不保存按钮")
        self.no_save_button.tap()
        log.logger.info("点击完毕")
        if self.base_parent.wait_activity(activities.ActivityNames.CAMERA2, 10):
            log.logger.info('成功进入拍照页')
            return True
        log.logger.error("进入拍照页失败")
        return False

    def tap_cancel_button(self):
        """
            Summary:
                点击取消按钮
        Returns:

        """
        log.logger.info("开始点击不保存按钮")
        self.no_save_button.tap()
        log.logger.info("点击完毕")
        time.sleep(3)

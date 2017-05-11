#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为底部弹层
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import text_view

from activities import activities

import time


class BottomPopupWindow(base_frame_view.BaseFrameView):
    """
        Summary:
            底部的弹层
    """

    popup_id = 'android:id/content'

    def __init__(self, parent, **kwargs):
        super(BottomPopupWindow, self).__init__(parent)
        if kwargs:
            self._linear_layout = linear_layout.LinearLayout(self.parent, **kwargs)
        else:
            self._linear_layout = linear_layout.LinearLayout(self.parent, id=self.popup_id)

    def __getattr__(self, item):

        if hasattr(self._linear_layout, item):
            return getattr(self._linear_layout, item)
        return getattr(self.base_parent, item)

    @property
    def save_temporary(self):
        """
            Summary:
                临时保存按钮
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_confirm'
        return text_view.TextView(self._linear_layout, id=id_)

    @property
    def no_save(self):
        """
            Summary:
                不保存
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_negative'
        return text_view.TextView(self._linear_layout, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                返回对话框上的取消按钮
        """
        id_ = 'com.jiuyan.infashion:id/publish_menu_save_tmp_cancel'
        return text_view.TextView(self._linear_layout, id=id_)

    # *************************操作方法**********************

    def tap_save_tmp(self):
        """
            Summary:
                点击临时保存
        """
        log.logger.info("开始点击临时保存按钮")
        self.save_temporary.tap()
        log.logger.info("完成临时保存按钮的点击")
        if self.base_parent.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
            log.logger.info("成功进入图片选择页")
            return True
        log.logger.error("进入图片选择页失败")
        return False

    def tap_no_save(self):
        """
            Summary:
                点击不保存按钮
        """
        log.logger.info("开始点击不保存按钮")
        self.no_save.tap()
        log.logger.info("完成不保存按钮的点击")
        if self.base_parent.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
            log.logger.info("成功进入图片选择页")
            return True
        log.logger.error("进入图片选择页失败")
        return False

    def tap_cancel(self, activity=None):
        """
            Summary:
                    点击不保存按钮
        """
        log.logger.info("开始点击取消按钮")
        self.no_save.tap()
        log.logger.info("完成取消按钮的点击")
        if activity:
            if self.base_parent.wait_activity(activity, 10):
                log.logger.info("成功停留在当前页面")
                return True
            log.logger.error("停留失败")
            return False
        return True

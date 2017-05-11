#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 图片编辑裁剪页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_view

from activities import activities


class CropperImageActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            图片编辑裁剪页面

        Attributes:

    """
    name = '.lib.component.cropper.CropperActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(CropperImageActivity, self).__init__(parent)
        self.__frame_view = frame_layout.FrameLayout(self.parent, id='android:id/content')

    @property
    def cancel_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = "com.jiuyan.infashion:id/btn_back"
        return image_view.ImageView(self.__frame_view, id=id_)

    @property
    def ok_button(self):
        """
            Summary:
                确认按钮
        """
        id_ = "com.jiuyan.infashion:id/btn_next"
        return image_view.ImageView(self.__frame_view, id=id_)

    # ************************操作***************************

    def tap_ok_button(self, window_name=None, timeout=10):
        """
            Summary:
                点击下一步按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击确认按钮")
        self.ok_button.tap()
        window_name = window_name or activities.ActivityNames.USER_INFO
        if self.wait_activity(window_name, timeout):
            log.logger.info("成功进入编辑资料页")
            return True
        else:
            log.logger.error("进入编辑资料页失败")
            return False

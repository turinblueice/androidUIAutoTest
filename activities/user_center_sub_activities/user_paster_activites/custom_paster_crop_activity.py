#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-我的贴纸-点击添加贴纸-制作自定义贴纸页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import text_view
from activities import activities


class CustomPasterCropActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-我的贴纸-制作自定义贴纸

        Attributes:

    """
    name = '.module.paster.custom.activities.CustomPasterCropActivity'

    def __init__(self, parent):
        super(CustomPasterCropActivity, self).__init__(parent)

    # ***********************引导提示部分************************
    @property
    def create_my_paster_button(self):
        """
            Summary:
                制作贴纸按钮
        """
        id_ = 'com.jiuyan.infashion:id/btn_guide_ok'
        return button.Button(self.parent, id=id_)

    # ************************操作方法***************************

    def tap_create_my_paster_button(self):
        """
            Summary:
                点击制作我的贴纸按钮
            Args:
                auto: 自动识别是否首次点击，若是首次，则点击tip进入图片选择页面
                Is_first：是否首次点击
        :return:
        """
        log.logger.info("点击立即制作我的自定义贴纸按钮")
        self.create_my_paster_button.tap()
        log.logger.info("完成点击立即制作我的自定义贴纸按钮")
        if self.wait_activity(activities.ActivityNames.SELECT_PHOTO_GUIDE, 5):
            log.logger.info("成功进入贴纸选择导航页")
            return True
        log.logger.error("进入贴纸选择导航页失败")
        return False

    # **************************裁剪区域部分***********************************
    @property
    def continue_button(self):
        """
            Summary:
                继续按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/transition_common_navigation_bar_right'
        return text_view.TextView(self.parent, id=id_)

    def tap_continue_button(self):
        """
            Summary:
                点击继续按钮
        :return:
        """
        log.logger.info("开始点击继续按钮")
        self.continue_button.tap()
        log.logger.info("继续按钮点击完毕")
        if self.wait_activity(activities.ActivityNames.CUT_OUT_PASTER, 10):
            log.logger.info("已经进入贴纸裁剪页面")
            return True
        log.logger.error("进入贴纸裁剪页面失败")
        return False


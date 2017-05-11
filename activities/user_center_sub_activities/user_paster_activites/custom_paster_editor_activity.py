#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-我的贴纸-点击添加贴纸-搭配贴纸

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import text_view
from activities import activities


class CustomPasterEditorActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-我的贴纸-制作自定义贴纸-搭配贴纸

        Attributes:

    """
    name = '.module.paster.custom.activities.CustomPasterEditorActivity'

    def __init__(self, parent):
        super(CustomPasterEditorActivity, self).__init__(parent)

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
            Summray:
                点击继续按钮
        """
        log.logger.info("开始点击继续按钮")
        self.continue_button.tap()
        log.logger.info("完成继续按钮点击")
        if self.wait_activity(activities.ActivityNames.PASTER_MALL, 20):
            log.logger.info("成功进入我的贴纸页面")
            return True
        log.logger.error("进入我的贴纸页失败")
        return False
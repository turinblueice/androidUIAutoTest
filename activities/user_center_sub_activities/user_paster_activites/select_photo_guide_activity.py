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
from activities import activities


class SelectPhotoGuideActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            选择照片/图片的引导页

        Attributes:

    """
    name = '.module.paster.custom.activities.SelectPhotoGuideActivity'

    def __init__(self, parent):
        super(SelectPhotoGuideActivity, self).__init__(parent)

    @property
    def guide_tip(self):
        """
            Summary:
                引导语
        """
        type_ = 'android.widget.TextView'
        return button.Button(self.parent, type=type_)

    # ************************操作方法***************************

    def tap_guide_tip(self):
        """
            Summary:
                点击引导语
        :return:
        """
        log.logger.info("点击引导语")
        self.guide_tip.tap()
        log.logger.info("完成引导语点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_PICKER, 10):
            log.logger.info("成功进入图片选择页")
            return True
        else:
            log.logger.info("进入图片选择页失败")
            return False

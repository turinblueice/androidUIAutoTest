#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:图片集合页

Authors: Turinblueice
Date: 2016/9/10
"""

from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import edit_text

from appium.webdriver import WebElement
from appium.webdriver.common import touch_action
from selenium.webdriver.common.touch_actions import TouchActions
from activities import activities
import time


class PersonalPhotoAlbumActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            图片集合页
            in记-点击相片-进入相册详情

        Attributes:

    """
    name = '.photo.PhotoCoreActivity'  # 图片详情页名称

    def __init__(self, parent):
        super(PersonalPhotoAlbumActivity, self).__init__(parent)
        #  等待页面网络请求进行初始化
        self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/toolbar')
        self._scroll_view = frame_layout.FrameLayout(self.parent, id='com.jiuyan.infashion:id/vp_photo_detail')

    @property
    def title(self):
        """
            Summary:
                活动页标题
        """
        id_ = 'com.jiuyan.infashion:id/tv_title'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def user_avatar(self):
        """
            Summary:
                用户头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_left'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def photo_list(self):
        """
            Summary:
                照片集列表
        :return:
        """
        xpath_ = '//android.view.View[@resource-id=\"com.jiuyan.infashion:id/photo_nine_cell\"]/' \
                 'android.widget.FrameLayout'
        return frame_layout.FrameLayoutList(self.base_parent, xpath=xpath_).frame_list

    # *********************************图片详情页图片底部信息*********************************

    @property
    def privacy_button(self):
        """
            Summary:
                隐私权限按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_photo_detail_privacy'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def zan_button(self):
        """
            Summary:
                点赞按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_photo_detail_like'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def zan_count(self):
        """
            Summary:
                点赞数
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/civ_photo_detail_like_num'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def more_menu(self):
        """
            Summary:
                更多按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_photo_detail_more'
        return image_view.ImageView(self.parent, id=id_)

    # ******************************底部发送文字组件****************************************

    @property
    def input_words_box(self):
        """
            Summary:
                对这张图片说点什么
        """
        id_ = 'com.jiuyan.infashion:id/et_content'
        return edit_text.EditText(self.parent, id=id_)

    @property
    def send_button(self):
        """
            Summary:
                发送按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_send'
        return text_view.TextView(self.parent, id=id_)

    # **************************操作方法*****************************

    def tap_avatar(self):
        """
            Summary:
                点击头像
        Returns:

        """
        log.logger.info("开始点击头像")
        self.user_avatar.tap()
        log.logger.info("完成头像点击")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入个人信息in记页")
            return True
        log.logger.error("进入个人信息in记页失败")
        return False

    def tap_back_button(self):
        """
            Summary:
                点击返回按钮
        Returns:

        """
        log.logger.info("开始点击返回按钮")
        self.back_button.tap()
        log.logger.info("完成返回按钮点击")
        time.sleep(3)

    def tap_privacy_button(self):
        """
            Summary:
                点击更改权限按钮
        """
        log.logger.info("开始点击更改权限按钮")
        self.privacy_button.tap()
        log.logger.info("完成更改权限按钮点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_PRIVAC, 10):
            log.logger.info("成功进入权限更改页")
            return True
        log.logger.error("进入权限更改页面失败")
        return False

    def tap_more_menu(self):
        """
            Summary:
                点击更多按钮
        """
        log.logger.info("开始点击更多按钮")
        self.more_menu.tap()
        time.sleep(2)
        log.logger.info("点击更多按钮完毕")
        if self.wait_for_element_present_under_alert(self.base_parent, type='android.widget.HorizontalScrollView'):
            log.logger.info("成功吊起分享面板")
            return True
        log.logger.error('吊起分享面板失败')
        return False


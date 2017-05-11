#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:

Authors: Turinblueice
Date: 2016/7/26
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_button
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import button

from activities.register_sign_activities import login_friend_recommend_activity
from activities.register_sign_activities import login_guide_video_activity

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from activities import activities
from selenium.common.exceptions import TimeoutException

import time


class LoginMainActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        登陆活动页

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.login.MainActivity'

    def __init__(self, parent):
        super(LoginMainActivity, self).__init__(parent)
        self.__current_fragment_id = 'com.jiuyan.infashion:id/base_fragment_id'
        self.__current_fragment = frame_layout.FrameLayout(self.parent, id=self.__current_fragment_id)

    @property
    def account_field(self):
        """
        Summary:
            帐号输入框

        """
        id_ = 'com.jiuyan.infashion:id/login_et_login_name'
        return edit_text.EditText(self.__current_fragment, id=id_)

    @property
    def password_field(self):
        """
        Summary:
            密码输入框
        """
        id_ = 'com.jiuyan.infashion:id/login_et_login_password'
        return edit_text.EditText(self.__current_fragment, id=id_)

    @property
    def login_guide_button(self):
        """
        开屏引导登录按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/login_and_register_btn_login'
        return text_view.TextView(self.__current_fragment, id=id_)

    @property
    def login_button(self):
        """
        Summary:
            登陆按钮
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_login'
        return text_view.TextView(self.__current_fragment, id=id_)

    @property
    def qq_login_buton(self):
        """
            Summary:
                QQ登录按钮
        Returns:

        """
        id_= 'com.jiuyan.infashion:id/login_tv_qq_btn'
        return text_view.TextView(self.__current_fragment, id=id_)

    @property
    def wechat_login_buton(self):
        """
            Summary:
                微信按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/login_tv_weixin_btn'
        return text_view.TextView(self.__current_fragment, id=id_)

    @property
    def weibo_login_buton(self):
        """
            Summary:
                新浪微博
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/login_tv_sina_btn'
        return text_view.TextView(self.__current_fragment, id=id_)

    @property
    def facebook_login_buton(self):
        """
            Summary:
                facebook登录按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/login_tv_facebook_btn'
        return text_view.TextView(self.__current_fragment, id=id_)

    # ***********************切换登陆页******************************
    @property
    def switch_account_button(self):
        """
            Summary:
                切换账号按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/login_tv_change_account'
        return text_view.TextView(self.parent, id=id_)

    @property
    def login_quick_button(self):
        """
            Summary:
                快速进入按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/login_tv_login'
        return text_view.TextView(self.parent, id=id_)

    # *************************登录引导页*******************************

    @property
    def camera_guide_login(self):
        """
            Summary:
                登录页的摄像头
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_guide_camera'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def skip_guide_login_button(self):
        """
            Summary:
                登录引导页的跳过，首次安装会出现
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_guide_skip'
        return text_view.TextView(self.parent, id=id_)

    @property
    def skip_dialogue_button(self):
        """
            Summary:
                弹出框的跳过按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/dialog_guide_camera_cancel'
        return text_view.TextView(self.parent, id=id_)

    @property
    def take_a_photo_dialogue_button(self):
        """
            Summary:
                弹出框的’拍一张‘按钮
        """
        id_ = 'com.jiuyan.infashion:id/dialog_guide_camera_confirm'
        return text_view.TextView(self.parent, id=id_)

    # ***********************操作方法*********************************
    def skip_to_login_main(self):
        """
            Summary:
                从切换按钮跳转到登陆主面板
        Returns:

        """
        log.logger.info("检查当前是否是登陆页的切换账号页")
        try:
            self.switch_account_button.is_displayed()
            log.logger.info("点击切换账号按钮")
            self.switch_account_button.tap()
            log.logger.info("点击完毕")
        except:
            log.logger.info("当前页面不是登陆切换账号页")
        finally:
            time.sleep(3)

    def input_account(self, phone_number):
        """
            Summary:
                在登陆页面输入账户手机号码

            Args:
                phone_number:手机号
        """
        log.logger.info("开始清空账号内容")
        self.account_field.clear_text_field()
        log.logger.info("账号内容清空完毕，开始输入账号")
        self.account_field.send_keys(phone_number)
        time.sleep(2)

    def input_password(self, password):
        """
            Summary:
                 在登陆页面输入密码
            Args:
                password:密码
        """
        log.logger.info("开始清空密码内容")
        self.password_field.clear_text_field()
        log.logger.info("密码内容清空完毕，开始输入密码")
        self.password_field.send_keys(password)
        time.sleep(2)

    def tap_login_guide_button(self, timeout=5):
        """
        点击登录引导按钮
        :param timeout:
        :return:
        """
        log.logger.info("开始点击登录引导按钮")
        self.login_guide_button.tap()
        log.logger.info("完成点击登录引导按钮")
        if self.wait_for_element_present(self.parent, timeout=5, id='com.jiuyan.infashion:id/login_tv_login'):
            log.logger.info("成功进入登陆页")
            return True
        log.logger.info("进入登录页失败")
        return False

    def tap_login_button(self, timeout=5, auto=True):
        """
            Summary:
                点击登陆按钮
            Args:
                timeout:最大等待时间
                interval:重试间隔
                auto:True:自动判断是否首次登录，是首次登录则会跳过引导页;False:默认非首次登录
        """
        log.logger.info("开始点击登录按钮")
        self.login_button.tap()
        log.logger.info("完成点击登录按钮")
        if auto:
            if self.wait_activity(activities.ActivityNames.LOGIN_GUIDE_VIDEO, timeout):
                log.logger.info("登录后首先进入了视频引导页")
                log.logger.info("点击跳过按钮")
                curr_friend_activity = login_guide_video_activity.LoginGuideVideoActivity(self.parent)
                curr_friend_activity.tap_skip_button(skip=True)

            #  点击登录按钮后，首先判断是否进入好友推荐页
            if self.wait_activity(activities.ActivityNames.LOGIN_FRIEND_RECOMMEND, timeout):
                log.logger.info("登录后首先进入了好友推荐页")
                log.logger.info("点击好友推荐页的完成按钮")
                curr_friend_activity = login_friend_recommend_activity.LoginFriendRecommendActivity(self.parent)
                curr_friend_activity.tap_finish_button()

            if self.wait_for_element_present_under_alert(
                    self.base_parent, timeout=3, id='com.jiuyan.infashion:id/tv_guide_skip'):

                log.logger.info("首次登录，进入引导页")
                log.logger.info("跳过引导页进入主页面")
                status = self.tap_skip_button()
                return status
            else:
                log.logger.info("无引导页,非首次登录")

        if self.wait_activity(activities.ActivityNames.IN_MAIN, 10):
            log.logger.info("登陆成功，成功进入In主页面")
            return True
        else:
            log.logger.info("登陆失败，进入In主页面失败")
            return False

    def tap_skip_button(self, skip=True):
        """
            Summary:
                跳过引导
            Args:
                skip:True:点击提示框的跳过按钮，False：点击提示框的拍一张按钮
        """
        log.logger.info("点击跳过引导页")
        self.skip_guide_login_button.tap()
        log.logger.info("点击完毕")
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.presence_of_element_located(
                    (MobileBy.ID, 'com.jiuyan.infashion:id/dialog_guide_camera_content'))
            )
            log.logger.info("弹出了提示框")
            if skip:
                log.logger.info("点击提示框的跳过按钮")
                self.skip_dialogue_button.tap()
                log.logger.info("点击完毕")
                if self.wait_activity(activities.ActivityNames.IN_MAIN, 10):
                    log.logger.info("成功进入In主页")
                    return True
                log.logger.error("进入In主页失败")
                return False
            else:
                log.logger.info("点击拍一张按钮")
                self.take_a_photo_dialogue_button.tap()
                log.logger.info("点击完毕")
                if self.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
                    log.logger.info("成功进入图片选择页")
                    return True
                log.logger.error("进入图片选择页失败")
                return False
        except TimeoutException:
            log.logger.error("没有出现提示框")
            return False

    def tap_qq_login_button(self):
        """
            Summary:
                点击QQ登录
        Returns:

        """
        log.logger.info("开始点击QQ登录按钮")
        self.qq_login_buton.tap()
        log.logger.info("QQ登录点击完毕")
        if self.wait_activity(activities.ActivityNames.QQ_AUTH, 10):
            log.logger.info("成功进入QQ登录页")
            return True
        log.logger.error("进入QQ登录页失败")
        return False

    def tap_weibo_login_button(self, auth=True, login=True):
        """
            Summary:
                点击QQ登录
            Args:
                auth:True:微博账号已授权;False:未授权
                login:True:微博客户端已登录;False:微博客户端未登录
        Returns:

        """

        log.logger.info("开始点击微博登录按钮")
        self.weibo_login_buton.tap()
        log.logger.info("微博登录点击完毕")
        if auth and login:
            if self.wait_activity(activities.ActivityNames.LOGIN_FRIEND_RECOMMEND, 10):
                log.logger.info("成功进入好友推荐页")
                return True
            log.logger.error("进入好友推荐页失败")
            return False
        return False

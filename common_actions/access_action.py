#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 访问到达指定页面的操作集合

Authors: Turinblueice
Date: 2016/7/26
"""

import time

from activities import activities
from activities.common_activities import camera2_activity
from activities.common_activities import story_gallery_activity
from activities.in_main_activities import user_center_tab_activity
from activities.in_main_activities import discover_tab_activity
from activities.register_sign_activities import login_friend_recommend_activity
from activities.register_sign_activities import login_main_activity

from base import base_frame_view
from base import thread_device_pool
from gui_widgets.custom_widgets import bottom_tab_widget
from gui_widgets.custom_widgets import continue_popup_window
from util import config_initial, log


class AccessAction(object):

    def __init__(self, driver):
        self.__driver = driver
        self.__base_app = base_frame_view.BaseFrameView(self.__driver)
        self.__model_config = config_initial.config_parser

        # ******************多设备相关变量**********************

        self.__thread_number = thread_device_pool.ThreadDeviceInfoPool.get_current_thread_number()

    @property
    def current_activity(self):
        """
            Summary:
                当前活动页面
        """
        return self.__base_app.current_activity

    @staticmethod
    def wait_for_app_launch(wait_time=6):
        """
            Summary:
                等待APP启动完毕,到达展示的首页
            Args:
                wait_time:等待时长
        """
        log.logger.info("等待app启动")
        time.sleep(wait_time)

    def _wait_for_init(self, wait_time=10, wait_friend=True, wait_broadcast=True,
                       wait_ad=True):
        """
            Summary:
                等待页面初始化
            Args:
                wait_time:等待时长
                wait_friend: True:等待好友推荐页面
                wait_ad:True:等待广告页面
        """
        #  app启动时,启动页面首先为登录页
        log.logger.info("进行页面初始化")
        if self.__base_app.wait_for_element_present_under_alert(self.__driver, timeout=wait_time,
                                                                id='com.jiuyan.infashion:id/login_and_register_btn_login'):

            if self.__base_app.wait_for_element_present_under_alert(self.__driver, timeout=2,
                                                                    id='com.jiuyan.infashion:id/login_tv_change_account'):
                # 登录切换页面
                log.logger.info("当前为登陆切换页面")
                curr_login_activity = login_main_activity.LoginMainActivity(self.__base_app)
                log.logger.info("点击切换账号按钮")
                curr_login_activity.switch_account_button.tap(3)
            # 未登录，则等待登陆页初始化完毕
            # 进入登录页后，因为页面内容需要初始化，有一定延时，因此要继续检查登录按钮是否存在
            log.logger.info("进入in登陆页面")
            log.logger.info("in原生登录页面初始化完毕")

        else:

            # 应用启动时，默认已登录，直接进入主页
            # 因为主页内容需要网络请求来初始化，因此要继续检查底部tab列表，若“发现”tab被选中，则证明已经进入in的主页
            # 且底部栏已初始化完毕， xpath为“发现”tab的xpath
            log.logger.info("等待in主页面初始化")

            if wait_friend:
                log.logger.info("检查是否有好友推荐页")
                if self.__driver.wait_activity(activities.ActivityNames.LOGIN_FRIEND_RECOMMEND, wait_time):
                    log.logger.info("登录后首先进入了好友推荐页")
                    log.logger.info("点击好友推荐页的完成按钮")
                    curr_friend_activity = login_friend_recommend_activity.LoginFriendRecommendActivity(self.__base_app)
                    curr_friend_activity.tap_finish_button()

            if wait_broadcast:
                log.logger.info("检查是否有允许通知的提示遮罩")
                if self.__base_app.wait_for_element_present_under_alert(
                        self.__driver, timeout=3, id='com.jiuyan.infashion:id/in_base_dialog_close'):
                    log.logger.info("当前页面存在允许通知的遮罩")
                    log.logger.info("关闭通知遮罩")
                    curr_discover_activity = discover_tab_activity.DiscoverTabActivity(self.__base_app)
                    curr_discover_activity.broadcast_close_button.tap()

            if wait_ad:
                # 检查广告遮罩
                log.logger.info("检查广告遮罩")
                if self.__base_app.wait_for_element_present_under_alert(
                        self.__driver, timeout=3, id='com.jiuyan.infashion:id/iv_delegate_popup_dialog'):
                    log.logger.info("当前页面存在广告遮罩")
                    log.logger.info("点击非广告部分，关闭广告")
                    self.__base_app.tap_window_top()

            if self.__base_app.wait_for_element_present_under_alert(
                self.__driver, id='com.jiuyan.infashion:id/ll_tab'
            ):
                log.logger.info("in主页面初始化完毕")
            else:
                # 其他情况，则直接抛出异常，结束程序。如应用一直卡在启动页，或者在指定时间内in主页没初始化完毕
                log.logger.error("指定时间内in主页未初始化完毕")
                raise Exception("指定时间内in主页未初始化完毕")

        time.sleep(1)

    def go_to_discover_tab(self):
        """
            Summary:
                进入发现tab页面
        :return:
        """
        # 先等待页面初始化完毕
        log.logger.info("应用启动后等待首次展现的页面初始化完毕")
        self._wait_for_init()

        login_status = True  # 默认登录状态
        if self.current_activity == activities.ActivityNames.LOGIN_MAIN:  # 当前页面为登陆页
            log.logger.info("当前应用未登录，先登录应用")
            login_status = self.login()
            log.logger.info("登录成功后，再次等待in主页面初始化完毕")
            self._wait_for_init(wait_friend=False)

        if login_status:

            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            status = curr_tab_widget.tap_discover_tab()
            if status:
                log.logger.info("准备工作完毕，已成功进入发现tab页")
                return True
        log.logger.error("准备工作完毕，进入发现tab页失败")
        return False

    def go_to_focus_tab(self):
        """
            Summary:
                进入关注tab页面
        :return:
        """
        # 先等待页面初始化完毕
        log.logger.info("应用启动后等待首次展现的页面初始化完毕")
        self._wait_for_init()

        login_status = True  # 默认登录状态
        if self.current_activity == activities.ActivityNames.LOGIN_MAIN:  # 当前页面为登陆页
            log.logger.info("当前应用未登录，先登录应用")
            login_status = self.login()
            log.logger.info("登录成功后，再次等待in主页面初始化完毕")
            self._wait_for_init(wait_friend=False)

        if login_status:

            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            status = curr_tab_widget.tap_focus_tab()
            if status:
                log.logger.info("准备工作完毕，已成功进入关注tab页")
                return True
        log.logger.error("准备工作完毕，进入关注tab页失败")
        return False

    def go_to_user_center_tab(self):
        """
            Summary:
                进入in主页-中心tab

        """
        # 先等待页面初始化完毕
        log.logger.info("应用启动后等待首次展现的页面初始化完毕")
        self._wait_for_init()

        login_status = True  # 默认登录状态
        if self.current_activity == activities.ActivityNames.LOGIN_MAIN:  # 当前页面为登陆页
            log.logger.info("当前应用未登录，先登录应用")
            login_status = self.login()
            log.logger.info("登录成功后，再次等待in主页面初始化完毕")
            self._wait_for_init(wait_friend=False)

        if login_status:

            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            status = curr_tab_widget.tap_center_tab()
            if status:
                log.logger.info("准备工作完毕，已成功进入中心tab页")
                return True
        log.logger.error("准备工作完毕，进入中心tab页失败")
        return False

    def go_to_publish_story_tab(self):
        """
            Summary:
                进入发布故事集的tab页面
        """
        if self.go_to_discover_tab():
            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            if curr_tab_widget.tap_camera_tab(wait_bubble=False):
                log.logger.info("成功进入拍照页")
                # 2.9.9版本新增步骤
                curr_camera2_activity = camera2_activity.Camera2Activity(self.__base_app)

                if curr_camera2_activity.is_continue_popup_exist():
                    popup_window = continue_popup_window.ContinuePopupWindow(self.__base_app)
                    log.logger.info("点击新建按钮")
                    popup_window.tap_new_button()

                status = curr_camera2_activity.tap_album_button()
                if status:
                    curr_story_gallery_activity = story_gallery_activity.StoryGalleryActivity(self.__base_app)
                    if curr_story_gallery_activity.tap_story_tab():
                        log.logger.info("已成功进入故事集tab")
                        return True
        log.logger.error("进入故事集tab失败")
        return False

    def go_to_publish_photo_tab(self):
        """
            Summary:
                进入发布图片的tab页面
        """
        if self.go_to_discover_tab():
            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            if curr_tab_widget.tap_camera_tab(wait_bubble=False):
                log.logger.info("成功进入拍照页")
                # 2.9.9版本新增步骤
                curr_camera2_activity = camera2_activity.Camera2Activity(self.__base_app)
                if curr_camera2_activity.is_continue_popup_exist():
                    popup_window = continue_popup_window.ContinuePopupWindow(self.__base_app)
                    log.logger.info("点击新建按钮")
                    popup_window.tap_new_button()

                status = curr_camera2_activity.tap_album_button()
                if status:
                    log.logger.info("成功进入照片选择页")
                    curr_story_gallery_activity = story_gallery_activity.StoryGalleryActivity(self.__base_app)

                    if curr_story_gallery_activity.tap_photo_tab():
                        log.logger.info("已成功进入图片tab")
                        return True
        log.logger.error("进入图片tab失败")
        return False

    def go_to_in_diary_tab(self):
        """
            Summary:
                进入in记页面
        """
        # 先等待页面初始化完毕
        log.logger.info("应用启动后等待首次展现的页面初始化完毕")
        self._wait_for_init()

        login_status = True  # 默认登录状态
        if self.current_activity == activities.ActivityNames.LOGIN_MAIN:  # 当前页面为登陆页
            log.logger.info("当前应用未登录，先登录应用")
            login_status = self.login()
            log.logger.info("登录成功后，再次等待in主页面初始化完毕")
            self._wait_for_init(wait_friend=False)

        if login_status:

            curr_tab_widget = bottom_tab_widget.BottomTabWidget(self.__base_app)
            status = curr_tab_widget.tap_in_diary_tab()
            if status:
                log.logger.info("准备工作完毕，已成功进入in记tab页")
                return True
        log.logger.error("准备工作完毕，进入in记tab页失败")
        return False

    def go_to_my_paster(self):
        """
            Summary:
                进入我的贴纸页面
        """
        if self.go_to_user_center_tab():
            curr_user_center_activity = user_center_tab_activity.UserCenterTabActivity(self.__base_app)
            log.logger.info("将\"我的贴纸\"上滑到屏幕中")
            curr_user_center_activity.swipe_up_entire_scroll_view()
            if curr_user_center_activity.tap_paster_bar():
                return True
        return False

    def login(self):
        """
            Summary:
                登陆
        """
        curr_login_view = login_main_activity.LoginMainActivity(self.__base_app)

        if self.__base_app.wait_for_element_present(self.__driver, time=10, id='com.jiuyan.infashion:id/login_and_register_btn_login'):
            log.logger.info("成功进入登录引导页")

            if curr_login_view.tap_login_guide_button():

                log.logger.info("成功进入登录页")
                curr_login_view.input_account(self.__model_config.get('account', 'account'+str(self.__thread_number)))
                curr_login_view.input_password(self.__model_config.get('account', 'password'+str(self.__thread_number)))
                status = curr_login_view.tap_login_button()
                return status
        log.logger.error("20秒内没有进入登陆主页面")
        return False

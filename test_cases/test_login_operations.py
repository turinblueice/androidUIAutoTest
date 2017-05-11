#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:登录模块

Authors: Turinblueice
Date: 2016/7/26
"""

from activities.authority_activities import qq_auth_activity
from activities.in_main_activities import user_center_tab_activity
from activities.register_sign_activities import login_main_activity
from activities.user_center_sub_activities import user_setting_activity
from base import base_frame_view, devices_base_test
from common_actions import access_action
from util import log


class LoginTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(LoginTestCase, self).__init__(*args, **kwargs)

    # @classmethod
    # def setUpClass(cls):
    #
    #     cls.create_driver()
    #     log.logger.info("类执行创建driver")
    #
    # @classmethod
    # def tearDownClass(cls):
    #     if cls.driver:
    #         cls.driver.quit()

    def setUp(self):
        self.create_driver(self.debug_mode)
        access_action.AccessAction.wait_for_app_launch(12)

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()
    
    def test_login_operation(self):
        """
            test_cases/test_login_operations.py:LoginTestCase.test_login_operation
        Summary:
            登录case

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        common_action = access_action.AccessAction(self.get_driver())
        thread_number = self.get_current_thread_number()
        try:

            curr_login_activity = login_main_activity.LoginMainActivity(base_app)

            curr_login_activity.skip_to_login_main()

            account = self.config_model.get('account', 'account'+str(thread_number))
            password = self.config_model.get('account', 'password'+str(thread_number))
            curr_login_activity.input_account(account)
            curr_login_activity.input_password(password)

            log.logger.info("开始点击登录按钮")
            login_status = curr_login_activity.tap_login_button()

            log.logger.info("验证登录结果,登录是否跳转成功")
            self.assertTrue(login_status, "登陆失败", "输入账号密码登陆")

            common_action.go_to_user_center_tab()
            log.logger.info("进入用户中心tab页")
            curr_user_center_tab = user_center_tab_activity.UserCenterTabActivity(base_app)

            log.logger.info("向上滑动整个屏幕，使\"设置\"出现在屏幕中")
            curr_user_center_tab.swipe_up_entire_scroll_view()

            log.logger.info("点击设置栏")
            status = curr_user_center_tab.tap_settings_bar()
            self.assertTrue(status, "没有进入用户设置页面", "进入用户设置页")

            curr_user_setting_activity = user_setting_activity.UserSettingActivity(base_app)

            log.logger.info("向上滑动屏幕，使\"退出登录\"出现在屏幕中")
            curr_user_setting_activity.swipe_up_entire_scroll_view()
            status = curr_user_setting_activity.tap_logout_bar()
            self.assertTrue(status, "用户退出失败", "退出按钮退出")

        except Exception as exp:
            log.logger.error("发现异常, case:test_login_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'login', exp)

    # def test_logout_operation(self):
    #     """
    #         test_cases/test_login_operations.py:LoginTestCase.test_login_operation
    #     Summary:
    #         登出case
    #
    #     """
    #     base_app = base_frame_view.BaseFrameView(self.get_driver())
    #     try:
    #         common_action = access_action.AccessAction(self.get_driver())
    #         common_action.go_to_user_center_tab()
    #         log.logger.info("进入用户中心tab页")
    #         curr_user_center_tab = user_center_tab_activity.UserCenterTabActivity(base_app)
    #
    #         log.logger.info("向上滑动整个屏幕，使\"设置\"出现在屏幕中")
    #         curr_user_center_tab.swipe_up_entire_scroll_view()
    #
    #         log.logger.info("点击设置栏")
    #         status = curr_user_center_tab.tap_settings_bar()
    #         self.assertTrue(status, "没有进入用户设置页面")
    #
    #         curr_user_setting_activity = user_setting_activity.UserSettingActivity(base_app)
    #
    #         log.logger.info("向上滑动屏幕，使\"退出登录\"出现在屏幕中")
    #         curr_user_setting_activity.swipe_up_entire_scroll_view()
    #         status = curr_user_setting_activity.tap_logout_bar()
    #         self.assertTrue(status, "用户退出失败")
    #
    #     except Exception as exp:
    #         log.logger.error("发现异常, case:test_logout_operation执行失败")
    #         self.raise_exp_and_save_screen_shot(base_app, 'logout', exp)

    def test_3rd_party_login_operation(self):
        """
            test_cases/test_login_operations.py:LoginTestCase.test_3rd_party_login_operation
        Summary:
            第三方登录case

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        common_action = access_action.AccessAction(self.get_driver())
        try:

            curr_login_activity = login_main_activity.LoginMainActivity(base_app)

            curr_login_activity.skip_to_login_main()

            log.logger.info("开始点击QQ登录按钮")
            status = curr_login_activity.tap_qq_login_button()
            self.assertTrue(status, "进入QQ授权页面失败", "QQ登陆页面")

            curr_qq_auth_activity = qq_auth_activity.QQAuthActivity(base_app)
            status = curr_qq_auth_activity.tap_login_button()
            log.logger.info("验证QQ登录结果,登录是否跳转成功")
            self.assertTrue(status, "登陆失败")

            common_action.go_to_user_center_tab()
            log.logger.info("进入用户中心tab页")
            curr_user_center_tab = user_center_tab_activity.UserCenterTabActivity(base_app)

            log.logger.info("向上滑动整个屏幕，使\"设置\"出现在屏幕中")
            curr_user_center_tab.swipe_up_entire_scroll_view()

            log.logger.info("点击设置栏")
            status = curr_user_center_tab.tap_settings_bar()
            self.assertTrue(status, "没有进入用户设置页面")

            curr_user_setting_activity = user_setting_activity.UserSettingActivity(base_app)

            log.logger.info("向上滑动屏幕，使\"退出登录\"出现在屏幕中")
            curr_user_setting_activity.swipe_up_entire_scroll_view()
            status = curr_user_setting_activity.tap_logout_bar()
            self.assertTrue(status, "用户退出失败", "用户退出")

            log.logger.info("点击微博登录")
            log.logger.info("只考虑当前微博已登录并已授权的情况")

        except Exception as exp:
            log.logger.error("发现异常, case:test_3rd_party_login_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, '3rd_party_login', exp)

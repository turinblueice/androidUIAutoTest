#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:关注页操作模块

Authors: Turinblueice
Date: 2016/7/26
"""

import random

from activities import activities
from activities.in_main_activities import focus_tab_activity
from activities.personal_detail_activities import friend_photo_album_detail_activity
from base import base_frame_view, devices_base_test
from common_actions import access_action
from common_actions import mobile_keyevent_action

from util import log


class FocusTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(FocusTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        driver = self.create_driver(self.debug_mode)
        action = access_action.AccessAction(driver)

        action.wait_for_app_launch(6)
        action.go_to_focus_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    def test_focus_normal_operation(self):
        """
            test_cases/test_friends_operations.py:FocusTestCase.test_focus_normal_operation
        Summary:
            关注页操作:下拉刷新-分页加载-切换分类

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:

            curr_focus_activity = focus_tab_activity.FocusTabActivity(base_app)

            log.logger.info("向下滑动,下拉刷新")
            curr_focus_activity.swipe_down_entire_scroll_view()
            self.assertTrue(True, "下拉刷新失败", "关注页下拉刷新")

            log.logger.info("向上滑动, 加载多个页面")
            curr_focus_activity.swipe_up_entire_scroll_view()
            curr_focus_activity.swipe_up_entire_scroll_view()
            curr_focus_activity.swipe_up_entire_scroll_view()
            self.assertTrue(True, "上滑分页加载失败", "关注页分页加载")

        except Exception as exp:
            log.logger.error("发现异常, case:test_focus_normal_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'focus_normal', exp)

    def test_focus_user_card_operation(self):
        """
            test_cases/test_friends_operations.py:FocusTestCase.test_focus_user_card_operation
        Summary:
            关注页用户卡片操作:点击头像-点击图片-点赞-取消点赞-评论

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_focus_activity = focus_tab_activity.FocusTabActivity(base_app)
            if curr_focus_activity.is_contact_friends_exisit():
                log.logger.info("关闭通讯录好友提示")
                curr_focus_activity.tap_close_contact_button()

            curr_card_list = curr_focus_activity.card_list
            log.logger.info("对屏幕中第一个用户动态卡片进行处理")

            curr_card = curr_card_list[0]

            log.logger.info("点击头像")
            status = curr_card.tap_avatar()
            self.assertTrue(status, "进入用户in记页失败")
            action.back(activities.ActivityNames.IN_MAIN, 3)

            status = curr_card.tap_photo()
            self.assertTrue(status, "进入查看图片详情页失败", "关注页用户卡片点击照片")
            action.back(activities.ActivityNames.IN_MAIN, 3)

            curr_focus_activity.swipe_up_any_view(ratio=0.5)

            #  屏幕滑动,重新获取一次当前卡片
            curr_card = curr_card_list[0]
            log.logger.info("点赞")
            status = curr_card.tap_zan()
            self.assertTrue(status, '点赞失败', "关注页用户卡片点赞")

            log.logger.info("取消点赞")
            status = curr_card.remove_zan()
            self.assertTrue(status, '点赞按钮没取消', "关注页用户卡片取消点赞")

            log.logger.info("评论照片")
            log.logger.info('点击评论按钮')
            curr_card.tap_comment()

            expected_words = u'评论' + unicode(str(random.random() * 10000)[:4], 'utf8')
            curr_focus_activity.send_words_box.input_words(expected_words)
            curr_focus_activity.send_words_box.tap_send_button()

            # 获取刚发送的文本,为评论列表的最后一行
            log.logger.info("检查评论内容")
            actual_words = curr_card.comment_list[-1].text
            self.assertEqual(expected_words.encode('utf-8'), actual_words, "评论内容有误", "关注页用户卡片评论-评论内容")
            log.logger.info("评论内容检查完毕")

            log.logger.info("检查评论人")
            expected_user = self.config_model.get('account', 'user_name' + self.get_current_thread_number())
            actual_user = curr_card.comment_user_list[-1].text
            self.assertEqual(expected_user, actual_user, "评论人有误", "关注页用户卡片评论-评论人")
            log.logger.info("评论人检查完毕")

        except Exception as exp:
            log.logger.error("发现异常, case:test_focus_user_card_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'focus_user_card', exp)

    def test_focus_friend_photo_operation(self):
        """
            test_cases/test_friends_operations.py:FocusTestCase.test_focus_friend_photo_operation
            Summary:
                发现-进入好友图片详情页-图片详情页操作-点击图片/头像/点赞/评论

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_focus_activity = focus_tab_activity.FocusTabActivity(base_app)

            if curr_focus_activity.is_contact_friends_exisit():
                log.logger.info("关闭通讯录好友提示")
                curr_focus_activity.tap_close_contact_button()

            curr_card_list = curr_focus_activity.card_list

            log.logger.info("点击首张卡片头部栏跳转")
            status = curr_card_list[0].tap_header_bar()
            self.assertTrue(status, "进入好友图片页失败", "关注页人物卡片点击头部栏")

            curr_photo_activity = friend_photo_album_detail_activity.FriendPhotoDetailActivity(base_app)
            log.logger.info("点击图片")
            status = curr_photo_activity.tap_photo(0)
            self.assertTrue(status, "进入图片详情页失败", "关注-图片详情页点击图片")
            action.back(activities.ActivityNames.FRIEND_PHOTO_DETAIL)

            status = curr_photo_activity.tap_tag(0)
            self.assertTrue(status, "进入标签话题页失败", "关注-图片详情页点击标签")
            action.back(activities.ActivityNames.FRIEND_PHOTO_DETAIL)

            curr_photo_activity.swipe_up_any_view(0.4)
            status = curr_photo_activity.tap_zan()
            self.assertTrue(status, "点赞失败", "关注-图片详情页点赞")

            status = curr_photo_activity.remove_zan()
            self.assertTrue(status, "取消点赞失败", "关注-图片详情页取消点赞")

            status = curr_photo_activity.tap_avatar()
            self.assertTrue(status, "进入个人详情页失败", "关注-图片详情页点击头像")
            action.back(activities.ActivityNames.FRIEND_PHOTO_DETAIL)

            log.logger.info('发表评论')

            expected_words = u'评论' + unicode(str(random.random() * 10000)[:4], 'utf8')
            curr_photo_activity.input_comment(expected_words)
            curr_photo_activity.tap_send_button()

            log.logger.info("检查评论内容")
            curr_photo_activity.swipe_up_entire_scroll_view()
            actual_words = curr_photo_activity.latest_comment_value
            self.assertEqual(expected_words.encode('utf-8'), actual_words, "评论内容有误", "关注-图片详情页评论内容")
            log.logger.info("评论内容检查完毕")

            log.logger.info("检查评论人")
            expected_user = self.config_model.get('account', 'user_name' + self.get_current_thread_number())
            actual_user = curr_photo_activity.latest_comment_user
            self.assertEqual(expected_user, actual_user, "评论人有误", "关注-图片详情页评论人")
            log.logger.info("评论人检查完毕")

        except Exception as exp:
            log.logger.error("发现异常, case:test_focus_friend_photo_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'friend_photo', exp)

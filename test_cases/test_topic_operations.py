#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:话题操作case

Authors: Turinblueice
Date: 2016/7/26
"""

import random

from activities import activities
from activities.discover_details_activities import topic_detail_activity
from activities.discover_details_activities import topic_sqaure_activity
from activities.in_main_activities import discover_tab_activity
from activities.personal_detail_activities import friend_photo_album_detail_activity
from base import devices_base_test
from base import base_frame_view
from common_actions import access_action
from common_actions import mobile_keyevent_action

from util import log


class TopicTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(TopicTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        driver = self.create_driver(self.debug_mode)
        action = access_action.AccessAction(driver)

        action.wait_for_app_launch()
        action.go_to_discover_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    @staticmethod
    def _get_different_value(min_, max_, value):
        """
            Summary:
                获取在min_和max_之间,与value不相等的值
        Args:
            min_: 最小值
            max_: 最大值
            value: 基准值

        Returns:

        """

        ret_value = random.randint(min_, max_)
        while ret_value == value:
            ret_value = random.randint(min_, max_)

        return ret_value

    def test_send_topic_comment_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_send_topic_comment_operation
        Summary:
            选择话题评论

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            log.logger.info("选择话题")
            status = curr_discover_activity.select_hot_topic(1)
            self.assertTrue(status, "进入话题详情页失败", "发现页-进入话题")

            curr_topic_activity = topic_detail_activity.TopicDetailActivity(base_app)
            curr_topic_activity.swipe_up_entire_scroll_view()

            curr_hot_container = curr_topic_activity.hotest_container_list[0]
            status = curr_hot_container.tap_to_submit_comment()

            self.assertTrue(status, "进入图片详情页失败", "点击最热话题发表评论")

            curr_friend_photo_activity = friend_photo_album_detail_activity.FriendPhotoDetailActivity(base_app)
            input_comment = u'in喜欢这个'
            curr_friend_photo_activity.input_comment(input_comment)
            curr_friend_photo_activity.tap_send_button()
            curr_friend_photo_activity.tap_back_button()

            user_name = self.config_model.get('account', 'user_name'+self.get_current_thread_number())
            self.assertEqual(user_name+' '+input_comment.encode('utf8'),
                             curr_hot_container.latest_comment, "最新的发布文字和刚刚发布的文字不一致", "发表评论文字检测")

        except Exception as exp:
            log.logger.error("发现异常, case:test_send_topic_topic_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'send_topic', exp)

    # 双击尚未实现，暂时注释
    # def test_like_newest_photo_operation(self):
    #     """
    #         test_cases/test_topic_operations.py:TopicTestCase.test_like_newest_photo_operation
    #     Summary:
    #         选择话题评论
    #
    #     """
    #     base_app = base_frame_view.BaseFrameView(self.get_driver())
    #     try:
    #
    #         curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)
    #
    #         log.logger.info("选择话题")
    #         status = curr_discover_activity.select_hot_topic(1)
    #         self.assertTrue(status, "进入话题详情页失败")
    #
    #         curr_topic_activity = topic_detail_activity.TopicDetailActivity(base_app)
    #         curr_topic_activity.tap_newest_tab()
    #
    #         curr_topic_activity.swipe_up_half_scroll_view()
    #         curr_newest_photo = curr_topic_activity.newest_photo_album_list[0]
    #
    #         count = int(curr_newest_photo.like_count) if not curr_newest_photo.like_count == 'like' else 0
    #         curr_newest_photo.double_tap()
    #         self.assertEqual(count+1, int(curr_newest_photo.like_count), "点赞数不一致")
    #
    #     except Exception as exp:
    #         log.logger.error("发现异常, case:test_like_newest_photo_operation执行失败")
    #         self.raise_exp_and_save_screen_shot(base_app, 'like_photo', exp)

    def test_topic_square_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_topic_square_operation
        Summary:
            话题广场操作
            我的话题-点击话题
            分类话题-切换分类-点击话题
            推荐话题-分页加载-点击话题

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            curr_discover_activity.tap_hot_topic_icon()
            curr_topic_square_activity = topic_sqaure_activity.TopicSquareActivity(base_app)

            log.logger.info("点击我的tab")
            curr_topic_square_activity.tap_my_tab()

            my_topic_count = len(curr_topic_square_activity.my_topic_list)
            log.logger.info("我的话题数为{}个".format(my_topic_count))
            index = random.randint(0, my_topic_count-1)
            log.logger.info("点击第{}个话题".format(index+1))
            status = curr_topic_square_activity.my_topic_list[index].tap()
            self.assertTrue(status, "进入话题详情页失败", "热门话题-我的话题-进入话题详情页")
            action.back(activities.ActivityNames.TOPIC_SQUARE)

            log.logger.info("点击分类tab")
            curr_topic_square_activity.tap_category_tab()
            cate_count = len(curr_topic_square_activity.category_list)
            log.logger.info("话题类别数为{}个".format(cate_count))
            self.assertTrue(status, "切换话题tab", "热门话题-点击分类tab")

            index = random.randint(0, cate_count-1)
            log.logger.info("点击第{}个话题类别".format(index + 1))
            curr_topic_square_activity.category_list[index].tap(5)

            curr_topic = curr_topic_square_activity.topic_list[0]
            old_topic_name = curr_topic.topic_name
            log.logger.info("当前类别下第一个话题为\"{}\"".format(old_topic_name))

            log.logger.info("切换话题分类, 获取新的类别")

            index = self._get_different_value(0, cate_count-1, index)
            log.logger.info("切换话题类别,点击第{}个话题类别".format(index + 1))
            curr_topic_square_activity.category_list[index].tap(5)

            curr_topic = curr_topic_square_activity.topic_list[0]
            new_topic_name = curr_topic.topic_name
            log.logger.info("当前类别下第一个话题为\"{}\"".format(new_topic_name))

            self.assertNotEqual(old_topic_name, new_topic_name, "话题类别未切换", "热门话题-分类话题-切换话题分类")

            topic_count = len(curr_topic_square_activity.topic_list)
            log.logger.info("\"{}\"话题数为{}个".format(new_topic_name, topic_count))
            index = random.randint(0, topic_count - 1)
            log.logger.info("点击第{}个话题".format(index+1))
            status = curr_topic_square_activity.topic_list[index].tap()
            self.assertTrue(status, "进入话题页失败", "热门话题-分类话题-点击话题")
            action.back(activities.ActivityNames.TOPIC_SQUARE)

            log.logger.info("点击推荐tab")
            curr_topic_square_activity.tap_recommend_tab()
            curr_topic_square_activity.swipe_up_entire_scroll_view()
            self.assertTrue(True, "点击推荐tab", "热门话题-推荐话题-分页加载")

        except Exception as exp:
            log.logger.error("发现异常, case:test_topic_square_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'topic_square', exp)

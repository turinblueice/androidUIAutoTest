#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:发现页case

Authors: Turinblueice
Date: 2016/7/26
"""

from activities import activities
from activities.discover_details_activities import all_category_activity
from activities.discover_details_activities import essence_recommend_activity
from activities.discover_details_activities import talent_recommend_activity
from activities.in_main_activities import discover_tab_activity
from activities.personal_detail_activities import personal_main_activity
from activities.personal_detail_activities import personal_remark_activity
from base import devices_base_test
from base import base_frame_view
from common_actions import access_action
from common_actions import mobile_keyevent_action
from util import log


class DiscoverTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(DiscoverTestCase, self).__init__(*args, **kwargs)

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

    def test_search_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_search_operation
        Summary:
            搜索操作-搜索用户/话题-点击进入用户/话题页面

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            log.logger.info("点击搜索框")
            curr_discover_activity.tap_search_box()

            log.logger.info("进入搜索页面")
            curr_search_page = discover_tab_activity.SearchPage(base_app)

            search_value = 'infashiontest'
            action.send_string(search_value)

            log.logger.info("验证搜索结果列表出现")
            self.assertTrue(curr_search_page.is_search_result_exist(), "没有搜索结果", "发现页搜索用户")

            status = curr_search_page.user_list[0].tap()
            self.assertTrue(status, "进入用户in记页失败")

            action.back(activities.ActivityNames.IN_MAIN)

            log.logger.info("清空搜索框遗留内容")
            curr_search_page.top_search_bar.search_box.clear_text_field()
            action.send_proud_key()

            self.assertTrue(curr_search_page.is_search_result_exist(), "没有搜索结果", "发现页搜索话题")

            status = curr_search_page.tag_list[0].tap()
            self.assertTrue(status, "进入话题页失败")

            action.back(activities.ActivityNames.IN_MAIN)
            # curr_search_page.top_search_bar.input_search_value(search_value)

        except Exception as exp:
            log.logger.error("发现异常, case:test_send_topic_topic_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'send_topic', exp)

    def test_discover_skip_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_discover_skip_operation
        Summary:
            跳转操作-热门话题箭头跳转/切换图片分类/点击图片跳转/广告跳转/故事集跳转

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            log.logger.info("点击热门话题箭头跳转")
            status = curr_discover_activity.tap_hot_topic_icon()
            self.assertTrue(status, "进入话题广场页面失败", "进入话题广场")
            action.back(activities.ActivityNames.IN_MAIN)

            log.logger.info("向上滑动使图片栏固定在顶部")
            curr_discover_activity.swipe_up_entire_scroll_view()
            #curr_discover_activity.swipe_up_any_view(ratio=0.1)
            log.logger.info("切换图片分类")
            log.logger.info("点击最新tab")
            curr_discover_activity.newest_header_tab.tap()
            status = curr_discover_activity.is_square_item_exisit()
            self.assertTrue(status, "切换图片分类失败", "切换图片分类-最新")

            log.logger.info("点击最热tab")
            curr_discover_activity.hotest_header_tab.tap()
            status = curr_discover_activity.is_square_item_exisit()
            self.assertTrue(status, "切换图片分类失败", "切换图片分类-最热")

            status = curr_discover_activity.first_photo_item.tap()
            self.assertTrue(status, "进入图片详情页面失败", "发现页点击九宫格图片")
            action.back(activities.ActivityNames.IN_MAIN)

            if curr_discover_activity.first_live_item:
                # 存在直播,则进入直播页
                status = curr_discover_activity.first_live_item.tap()
                self.assertTrue(status, "进入直播页面失败")
                action.back(activities.ActivityNames.IN_MAIN)

            if curr_discover_activity.first_story_item:
                # 存在故事集,则进入故事集页
                status = curr_discover_activity.first_story_item.tap()
                self.assertTrue(status, "进入故事集详情页面失败", "发现页点击九宫格故事集")
                action.back(activities.ActivityNames.IN_MAIN)
            if curr_discover_activity.ad_item:
                status = curr_discover_activity.tap_ad()
                self.assertTrue(status, "进入广告页面失败", "发现页点击九宫格广告")
                action.back(activities.ActivityNames.IN_MAIN)

        except Exception as exp:
            log.logger.error("发现异常, case:test_send_topic_topic_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'send_topic', exp)

    def test_discover_normal_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_discover_normal_operation
        Summary:
            常规操作-下拉刷新/上滑动加载

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            log.logger.info("下拉刷新")
            curr_discover_activity.swipe_down_entire_scroll_view()
            self.assertTrue(True, "下拉刷新失败", "发现页下拉刷新")

            log.logger.info("向上滑动加载")
            curr_discover_activity.swipe_up_entire_scroll_view()
            curr_discover_activity.swipe_up_entire_scroll_view()
            curr_discover_activity.swipe_up_entire_scroll_view()
            self.assertTrue(True, "上滑分页加载失败", "发现页上滑分页加载")

        except Exception as exp:
            log.logger.error("发现异常, case:test_send_topic_topic_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'send_topic', exp)

    def test_talent_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_talent_operation
        Summary:
            发现首页-》点击九宫格箭头-》分类-》达人分类操作/点击头像/图片/关注

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            curr_discover_activity.swipe_up_entire_scroll_view()
            log.logger.info("点击九宫格箭头跳转")
            status = curr_discover_activity.tap_head_bar_more()
            self.assertTrue(status, "进入全部分类页面失败", "进入分类页")

            curr_cate_activity = all_category_activity.AllCategoryActivity(base_app)
            status = curr_cate_activity.tap_talent()
            self.assertTrue(status, "进入达人推荐页面失败", "进入推荐达人页")

            curr_talent_activity = talent_recommend_activity.TalentRecommendActivity(base_app)

            log.logger.info("点击切换达人分类")
            curr_talent_activity.category_list[1].tap()
            status = curr_talent_activity.wait_for_talent(6)
            self.assertTrue(status, "达人加载失败", "切换达人分类-第二类目")

            curr_talent_activity.category_list[3].tap()
            status = curr_talent_activity.wait_for_talent(6)
            self.assertTrue(status, "达人加载失败", "切换达人分类-第四类目")

            log.logger.info("点击达人图片")
            status = curr_talent_activity.talent_list[0].tap_image(0)
            self.assertTrue(status, "进入图片详情页失败", "点击达人图片")
            action.back(activities.ActivityNames.TALENT_RECOMMEND)

            log.logger.info("开始关注达人")
            status = curr_talent_activity.talent_list[1].tap_follow_button()
            self.assertTrue(status, "关注按钮没选中", "关注达人")

            log.logger.info("进入达人主页取消关注")
            log.logger.info("点击推荐达人的头像")
            status = curr_talent_activity.talent_list[1].tap_avatar()
            self.assertTrue(status, "进入达人主页失败", "点击达人头像")

            curr_personal_activity = personal_main_activity.PersonalMainActivity(base_app)
            curr_personal_activity.tap_unfollow_button()
            curr_personal_activity.tap_confirm_unfollow_button()

            self.assertEqual('+ 关注', curr_personal_activity.follow_button.text,
                             "取消关注未成功", "取消关注达人")

        except Exception as exp:
            log.logger.error("发现异常, case:test_talent_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'test_talent', exp)

    def test_essence_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_essence_operation
        Summary:
            发现首页-》点击九宫格箭头-》分类-》精选分类选择分类/点击图片/点赞

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            curr_discover_activity.swipe_up_entire_scroll_view()
            log.logger.info("点击九宫格箭头跳转")
            status = curr_discover_activity.tap_head_bar_more()
            self.assertTrue(status, "进入全部分类页面失败")

            curr_cate_activity = all_category_activity.AllCategoryActivity(base_app)
            curr_cate_activity.swipe_up_entire_scroll_view()

            curr_cate = curr_cate_activity.category_list[0]
            log.logger.info("点击精选分类的\"{}\"".format(curr_cate.text))
            curr_cate.tap()

            curr_essence_activity = essence_recommend_activity.EssenceRecommendActivity(base_app)

            log.logger.info("开始切换精选分类")
            curr_tab = curr_essence_activity.tab_list[2]
            log.logger.info("点击tab\"{}\"".format(curr_tab.text))
            curr_tab.tap(4)
            status = curr_essence_activity.wait_for_newest_photo_album(6)
            self.assertTrue(status, "新相册加载失败", "切换精选分类-第三个类目")

            curr_tab = curr_essence_activity.tab_list[0]
            log.logger.info("点击tab\"{}\"".format(curr_tab.text))
            curr_tab.tap(4)
            status = curr_essence_activity.wait_for_newest_photo_album(6)
            self.assertTrue(status, "新相册加载失败", "切换精选分类-第一个类目")

            log.logger.info("开始点赞")
            log.logger.info("对当前首张专辑进行点赞")
            status = curr_essence_activity.photo_list[0].tap_like_button()
            self.assertTrue(status, "点赞失败", "照片集点赞")

            log.logger.info("取消点赞")
            log.logger.info("对当前首张专辑取消点赞")
            status = curr_essence_activity.photo_list[0].tap_like_button(False)
            self.assertTrue(status, "点赞失败", "照片集取消点赞")

            log.logger.info("点击图片")
            status = curr_essence_activity.photo_list[1].tap()
            self.assertTrue(status, "进入个人相册详情页失败", "点击精选相册照片")

        except Exception as exp:
            log.logger.error("发现异常, case:test_essence_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'test_essence', exp)

    def test_friend_in_diary_operation(self):
        """
            test_cases/test_topic_operations.py:TopicTestCase.test_friend_in_diary_operation
        Summary:
            发现首页-》点击九宫格箭头-》分类-》达人分类操作->进入达人in记主页操作

        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:

            curr_discover_activity = discover_tab_activity.DiscoverTabActivity(base_app)

            curr_discover_activity.swipe_up_entire_scroll_view()
            log.logger.info("点击九宫格箭头跳转")
            status = curr_discover_activity.tap_head_bar_more()
            self.assertTrue(status, "进入全部分类页面失败")

            curr_cate_activity = all_category_activity.AllCategoryActivity(base_app)
            status = curr_cate_activity.tap_talent()
            self.assertTrue(status, "进入达人推荐页面失败")

            curr_talent_activity = talent_recommend_activity.TalentRecommendActivity(base_app)

            log.logger.info("点击推荐达人的头像")
            status = curr_talent_activity.talent_list[0].tap_avatar()
            self.assertTrue(status, "进入达人主页失败", "点击推荐达人头像")

            curr_personal_activity = personal_main_activity.PersonalMainActivity(base_app)

            log.logger.info("点击关注")
            status = curr_personal_activity.tap_follow_button()
            self.assertTrue(status, "关注对话框吊起失败", "在他人in记页点击关注达人")

            curr_follow_dialogue = curr_personal_activity.follow_dialogue
            curr_follow_dialogue.select_group('interest')  # 选择订阅分类
            curr_follow_dialogue.tap_ok_button()

            if curr_personal_activity.is_friends_recommend_exist():
                # 如果出现好友推荐,则点击收起按钮
                curr_personal_activity.tap_friends_pull_button()

            log.logger.info("进入更多页面")
            status = curr_personal_activity.tap_more_button()
            self.assertTrue(status, "进入更改页面失败", "进入他人in记资料更改页")

            curr_remark_activity = personal_remark_activity.PersonalRemarkActivity(base_app)
            log.logger.info("更换分组")
            status = curr_remark_activity.select_group('friends')
            self.assertTrue(status, "更换分组失败", "更换好友分组")

            log.logger.info("更换昵称")
            nick_name = 'nickname'
            curr_remark_activity.input_remark_name(nick_name)

            log.logger.info("点击头像")
            status = curr_remark_activity.tap_avatar()
            self.assertTrue(status, "点击头像失败", "资料更改页点击好友头像")

            action.back(activities.ActivityNames.REMARK)

            log.logger.info("点击完成")
            curr_remark_activity.tap_ok_button()

            log.logger.info("验证新更改的昵称")
            curr_username = curr_personal_activity.user_nickname
            self.assertEqual(curr_username, nick_name,
                             "昵称更改失败,原昵称\"{}\",新昵称\"{}\"".format(curr_username, nick_name), "更改备注名")
            log.logger.info("验证完毕")

            log.logger.info("点击照片")
            status = curr_personal_activity.matrix_photo_album_list[0].tap()
            self.assertTrue(status, "进入图片详情页失败", "他人in记页点击照片")
            action.back(activities.ActivityNames.DIARY_INFO)

            log.logger.info("取消关注")
            curr_personal_activity.tap_unfollow_button()
            curr_personal_activity.tap_confirm_unfollow_button()

            self.assertEqual('+ 关注', curr_personal_activity.follow_button.text,
                             "取消关注未成功", "他人in记页取消关注")

        except Exception as exp:
            log.logger.error("发现异常, case:test_friend_in_diary_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'friend_in_diary', exp)
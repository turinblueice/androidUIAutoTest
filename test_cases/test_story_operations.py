#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 发表故事集操作

Authors: Turinblueice(hongquan@itugo.com)
Date:    16/5/5 17:47
"""

import random

from activities.common_activities import story_gallery_activity
from activities.story_activities import story_edit_activity
from activities.story_activities import story_preview_activity
from activities.story_activities import story_setting_activity
from activities.story_activities import story_share_activity
from base import devices_base_test
from base import base_frame_view
from common_actions import access_action

from util import log


class StoryTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(StoryTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        self.create_driver(self.debug_mode)
        driver = self.get_driver()

        action = access_action.AccessAction(driver)
        action.wait_for_app_launch()
        action.go_to_publish_story_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    def test_publish_story_operation(self):
        """
            test_cases/test_story_operations.py:StoryTestCase.test_publish_story_operation
            Summary:
                发布故事集
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)

            #  当前页可见的按日期划分的相册列表
            curr_date_photo_albums = curr_gallery_activity.date_photo_albums

            #  为了排除底部相册集的干扰，这里选择第一个相册列表
            album_index = 0
            curr_photo_album_date, curr_photo_album = curr_date_photo_albums[album_index]

            #  当前选择的相册内的照片列表
            curr_photo_list = curr_photo_album[curr_gallery_activity.STORY_PHOTO]

            # 相册集中的照片，为了排除底部四张照片被遮罩tab的干扰，最多选择前12张
            max_photo_count = len(curr_photo_list) if len(curr_photo_list) < 12 else 12

            picked_count = random.randint(1, max_photo_count)  # 选择的照片数量
            log.logger.info("随机选择{}相册中的{}张照片".format(curr_photo_album_date, picked_count))

            for index in random.sample(xrange(max_photo_count), picked_count):
                log.logger.info("选择{}相册中的第{}张照片".format(curr_photo_album_date, index+1))
                curr_photo_list[index].select()
                log.logger.info("验证该图片有没有被选中")
                self.assertTrue(curr_photo_list[index].is_selected(), "该图片没有被选中",
                                "故事集-{}相册第{}张照片选中检测".format(curr_photo_album_date, index+1))
                log.logger.info("该图片已被选中")

            log.logger.info("验证已选中的图片的数目")
            self.assertEqual(str(picked_count), curr_gallery_activity.selected_photo_count, "选择的图片数量不一致",
                             "故事集-选中照片的数目检测")

            curr_gallery_activity.tap_story_next_step_button()

            curr_story_edit_activity = story_edit_activity.StoryEditActivity(base_app)
            curr_story_edit_activity.diary_cover_detail.input_diary_name(u'第一篇文章')
            curr_story_edit_activity.diary_cover_detail.input_diary_beginning(u'文章开头')
            curr_story_edit_activity.tap_preview_button()

            curr_story_preview_activity = story_preview_activity.StoryPreviewActivity(base_app)
            curr_story_preview_activity.tap_next_button()

            curr_story_setting_activity = story_setting_activity.StorySettingActivity(base_app)
            curr_story_setting_activity.tap_finish_button()

            curr_story_share_activity = story_share_activity.StoryShareActivity(base_app)
            self.assertTrue(curr_story_share_activity.is_publish_success(), "发布日记未成功", "故事集-发布故事集")

            status = curr_story_share_activity.tap_close_button()
            self.assertTrue(status, "进入in主页失败", "关闭刚发布的故事集")

        except Exception as exp:
            log.logger.error("发现异常, case:test_publish_story_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'publish_story', exp)

    def test_publish_story_from_in_gallery_operation(self):
        """
            test_cases/test_story_operations.py:StoryTestCase.test_publish_story_from_in_gallery_operation
            Summary:
                发布故事集-点击写故事-点击照片-点击in记相册选择照片上传
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)

            #  点击上方相册选择列表选择IN相册
            curr_gallery_activity.tap_album_droplist()
            curr_gallery_activity.tap_in_diary_album()
            log.logger.info("随机选择几张照片")
            indexes = [1, 3, 4]
            curr_gallery_activity.select_photo_from_in_diary(indexes)

            log.logger.info("验证已选中的图片的数目")
            self.assertEqual(str(len(indexes)), curr_gallery_activity.selected_photo_count, "选择的图片数量不一致",
                             "故事集-in记相册选中图片数目检测")

            curr_gallery_activity.tap_story_next_step_button()

            curr_story_edit_activity = story_edit_activity.StoryEditActivity(base_app)
            curr_story_edit_activity.diary_cover_detail.input_diary_name(u'in记相册发布文章')
            curr_story_edit_activity.diary_cover_detail.input_diary_beginning(u'in记相册发布文章，发布文章开头')
            curr_story_edit_activity.tap_preview_button()

            curr_story_preview_activity = story_preview_activity.StoryPreviewActivity(base_app)
            curr_story_preview_activity.tap_next_button()

            curr_story_setting_activity = story_setting_activity.StorySettingActivity(base_app)
            curr_story_setting_activity.tap_finish_button()

            curr_story_share_activity = story_share_activity.StoryShareActivity(base_app)
            self.assertTrue(curr_story_share_activity.is_publish_success(), "发布日记未成功", "故事集-in记相册发布故事集")

            status = curr_story_share_activity.tap_close_button()
            self.assertTrue(status, "进入in主页失败", "关闭刚发布的in记相册故事集")

        except Exception as exp:
            log.logger.error("发现异常, case:test_publish_story_from_in_gallery_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'publish_story_from_in_gallery', exp)

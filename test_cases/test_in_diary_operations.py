#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: in记操作

Authors: Turinblueice(hongquan@itugo.com)
Date:    16/5/5 17:47
"""

import random

from activities import activities
from activities.common_activities import cropper_image_activity
from activities.common_activities import photo_picker_activity
from activities.friend_activities import fans_list_activity
from activities.personal_detail_activities import personal_main_activity
from activities.personal_detail_activities import personal_photo_album_activity
from base import base_frame_view, devices_base_test
from common_actions import access_action
from util import log


class InDiaryTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(InDiaryTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        driver = self.create_driver(self.debug_mode)

        action = access_action.AccessAction(driver)
        action.wait_for_app_launch()
        action.go_to_in_diary_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    def test_in_diary_self_operation(self):
        """
            test_cases/test_in_diary_self_operations.py:InDiaryTestCase.test_in_diary_self_operation
            Summary:
                个人in记操作
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            in_diary_activity = personal_main_activity.PersonalMainActivity(base_app)

            log.logger.info("进入in记页面")

            fans_count = in_diary_activity.fans_number
            log.logger.info("当前用户粉丝总数为{}".format(fans_count))

            log.logger.info("点击粉丝,进入粉丝列表页")
            status = in_diary_activity.tap_fans_button()
            self.assertTrue(status, "进入粉丝列表失败", "个人IN记进入粉丝列表页")

            curr_fans_list_activity = fans_list_activity.FansListActivity(base_app)
            curr_fans_list = curr_fans_list_activity.fans_list
            if curr_fans_list and len(curr_fans_list) > 0:
                log.logger.info("点击进入粉丝in记页")
                status = curr_fans_list[0].tap()
                self.assertTrue(status, "进入粉丝in记页面失败", "粉丝列表页进入粉丝IN记页")
                log.logger.info("点击后退回到原页面")
                curr_in_diary_activity = personal_main_activity.PersonalMainActivity(base_app)
                curr_in_diary_activity.tap_back_button()
            curr_fans_list_activity.tap_back_button()

            curr_photo_album = in_diary_activity.timeline_photo_album_list[0]
            curr_month = curr_photo_album.month
            curr_date = curr_photo_album.date
            log.logger.info("当前照片显示模式为时间线,第一组照片时间为\"{}{}\"".format(curr_month,curr_date))
            log.logger.info("检查照片组数展示")
            in_diary_activity.swipe_up_entire_scroll_view()
            timeline_photo_album_list = in_diary_activity.timeline_photo_album_list
            log.logger.info("当前屏幕中时间线照片组数为{}".format(len(timeline_photo_album_list)))
            self.assertTrue(True, "时间线模式看照片", "时间线模式查看照片")

            log.logger.info("点击看图模式切换按钮")
            in_diary_activity.tap_switch_button()
            log.logger.info("完成看图模式切换,现在为矩阵模式")
            self.assertTrue(True, "看图模式看照片", "看图模式查看照片")

            status = in_diary_activity.matrix_photo_album_list[1].tap(tap_count=2)
            self.assertTrue(status, "进入图片详情页失败", "看图模式点击照片")

            curr_photo_album_detail_activity = personal_photo_album_activity.PersonalPhotoAlbumActivity(base_app)
            curr_photo_album_detail_activity.tap_back_button()

            in_diary_activity.swipe_down_entire_scroll_view()

            log.logger.info("开始更换封面")
            in_diary_activity.tap_diary_cover()
            in_diary_activity.tap_change_cover_button()

            curr_photo_picker_activity = photo_picker_activity.PhotoPickerActivity(base_app)

            image_count = len(curr_photo_picker_activity.post_image_list)
            max_index = image_count if image_count < 11 else 11
            index = random.randint(2, max_index)
            curr_photo_picker_activity.select_image(index)
            curr_photo_picker_activity.tap_next_step_button()

            curr_cropper_activity = cropper_image_activity.CropperImageActivity(base_app)
            status = curr_cropper_activity.tap_ok_button(activities.ActivityNames.IN_MAIN)
            self.assertTrue(status, "回到in记页面失败", "更换个人IN记封面")

            log.logger.info("更换封面任务完成")

        except Exception as exp:
            log.logger.error("发现异常, case:test_in_diary_self_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'in_diary_self', exp)


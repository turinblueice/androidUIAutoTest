#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 发表图片操作

Authors: Turinblueice(hongquan@itugo.com)
Date:    16/5/5 17:47
"""

import random

from activities import activities
from activities.common_activities import camera2_activity
from activities.common_activities import story_gallery_activity
from activities.publish_activities import publish_activity
from activities.publish_activities import publish_core_activity
from activities.publish_activities import publish_words_art_activity
from activities.publish_activities import publish_words_tag_activity
from activities.user_center_sub_activities.user_paster_activites import user_paster_activity
from base import devices_base_test
from base import base_frame_view
from common_actions import access_action
from common_actions import mobile_keyevent_action
from gui_widgets.custom_widgets import bottom_popup_art_text_window
from util import log


class PhotoTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(PhotoTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        driver = self.create_driver(self.debug_mode)

        action = access_action.AccessAction(driver)
        action.wait_for_app_launch(5)
        action.go_to_publish_photo_tab()

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    def test_publish_photo_operation(self):
        """
            test_cases/test_photo_operations.py:PhotoTestCase.test_publish_photo_operation
            Summary:
                发布图片
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)

            log.logger.info("切换一次底部tab，避免\"发布故事集\"的引导遮罩对选取图片的干扰")
            curr_gallery_activity.tap_story_tab()
            curr_gallery_activity.tap_photo_tab()

            #  当前图片tab下的图片列表
            curr_photo_list = curr_gallery_activity.image_photo_list
            photo_count = curr_gallery_activity.image_photo_enable_picked_count

            picked_count = 3
            log.logger.info("随机选{}张图片".format(picked_count))

            #  选随机选择几张图片,为了排除底部遮罩tab的干扰，图片最多选择11张
            max_pick_count = photo_count if photo_count < 11 else 11
            for index, photo_index in enumerate(random.sample(xrange(max_pick_count), picked_count)):
                log.logger.info("选择第{}张照片,相册中的第{}张照片".format(index+1, photo_index+1))
                curr_photo_list[photo_index].select()
                log.logger.info("验证该图片有没有被选中")
                self.assertEqual(str(index+1), curr_photo_list[photo_index].check_value, "该图片没有被选中",
                                 "发布图片-第{}张图片选中序号{}检测".format(photo_index+1, index+1))
                log.logger.info("该图片已被选中")

            log.logger.info("验证已选中的图片的数目")
            self.assertEqual(str(picked_count), curr_gallery_activity.selected_photo_count, "选择的图片数量不一致",
                             "发布图片-选中图片数目检测")

            curr_gallery_activity.tap_photo_next_step_button()

            curr_publish_core_activity = publish_core_activity.PublishCoreActivity(base_app)

            if curr_publish_core_activity.is_guide_mask_exist() or curr_publish_core_activity.is_sticker_mask_exist():
                log.logger.info("存在引导遮罩,移除引导遮罩")
                curr_publish_core_activity.remove_guide_mask()

            log.logger.info("验证发布加工页的图片数")
            self.assertEqual(picked_count, len(curr_publish_core_activity.photo_available_list),
                             "发布加工页面图片数目不正确", "发布图片-发布加工页图片数目检测")

            # ***********标签检测*********************
            log.logger.info('点击标签按钮,吊起标签遮罩')
            status = curr_publish_core_activity.tap_mark_tool()
            self.assertTrue(status, '吊起标签失败')

            log.logger.info('点击文字标签')
            status = curr_publish_core_activity.tap_words_tag()
            self.assertTrue(status, "进入文字标签页失败")

            curr_words_tag_activity = publish_words_tag_activity.PublishWordsTagActivity(base_app)
            curr_words_tag_activity.input_words(u'庐山升龙霸')
            curr_words_tag_activity.tap_add_button()

            self.assertTrue(curr_words_tag_activity.is_tag_added_successful(), '标签添加失败', "添加文字标签")

            curr_publish_core_activity.tap_finish_button()

            curr_publish_activity = publish_activity.PublishActivity(base_app)
            log.logger.info("验证发布的图片数量")
            self.assertEqual(picked_count, len(curr_publish_activity.photo_available_list), "发布贴纸数量不正确",
                             "发布页图片数目检测")

            log.logger.info("发布页点击返回按钮")
            status = curr_publish_activity.tap_back_button()
            self.assertTrue(status, "回到发布加工页失败")

            curr_publish_core_activity.tap_finish_button()

            curr_publish_activity.input_words(u"测试图片发布")
            curr_publish_activity.tap_publish_button()

            log.logger.info("开始验证发布情况")
            status = curr_publish_activity.is_publish_successful()
            self.assertTrue(status, "发布失败", "发布图片")

        except Exception as exp:
            log.logger.error("发现异常, case:test_publish_photo_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'publish_photo', exp)

    def test_take_photo_operation(self):
        """
            test_cases/test_photo_operations.py:PhotoTestCase.test_take_photo_operation
            Summary:
                拍照-选中拍照的图片-进入加工-返回-临时保存
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:
            action.back(activities.ActivityNames.CAMERA2)
            curr_camera2_activity = camera2_activity.Camera2Activity(base_app)
            log.logger.info("点击拍照")
            status = curr_camera2_activity.tap_camera()
            self.assertTrue(status, "拍照失败", "点击拍照")

            log.logger.info("点击拍照完成按钮")
            status = curr_camera2_activity.tap_finish_camera()
            self.assertTrue(status, "拍照完成失败", "加工拍照图片")

            # 2.9.9之前版本的步骤
            # curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)
            #
            # log.logger.info("切换一次底部tab，避免\"发布故事集\"的引导遮罩对选取图片的干扰")
            # curr_gallery_activity.tap_story_tab()
            # curr_gallery_activity.tap_photo_tab()
            #
            # status = curr_gallery_activity.open_camera()
            # self.assertTrue(status, "进入故事照片编辑页失败", "进入拍照页")
            #
            # log.logger.info('点击拍照')
            # curr_story_camera_activity = story_camera_activity.StoryCameraActivity(base_app)
            # curr_story_camera_activity.tap_camera()

            # log.logger.info('选中刚拍照的图片')
            # curr_story_camera_activity.photo_list[0].select()
            # self.assertTrue(curr_story_camera_activity.photo_list[0].is_selected, '刚拍的照片没选中', "拍照并选中刚拍的照片")
            #
            # curr_story_camera_activity.tap_next_step_button()

            curr_publish_core_activity = publish_core_activity.PublishCoreActivity(base_app)

            log.logger.info("验证返回按钮,返回拍照编辑页")
            curr_publish_core_activity.tap_back_button(save=False, cancel=False)

        except Exception as exp:
            log.logger.error("发现异常, case:test_take_photo_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'take_photo', exp)

    def test_take_and_pick_photo_operation(self):
        """
            test_cases/test_photo_operations.py:PhotoTestCase.test_take_and_pick_photo_operation
            Summary:
                拍照同时选中已有的图片-进入编辑加工页
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        action = mobile_keyevent_action.KeyEventAction(self.get_driver())
        try:
            action.back(activities.ActivityNames.CAMERA2)
            curr_camera2_activity = camera2_activity.Camera2Activity(base_app)
            log.logger.info("点击拍照")
            curr_camera2_activity.tap_camera()

            log.logger.info("点击拍照完成按钮")
            curr_camera2_activity.tap_finish_camera()

            curr_publish_core_activity = publish_core_activity.PublishCoreActivity(base_app)
            self.assertTrue(curr_publish_core_activity.photo_available_list[0].is_selected, "拍照的照片在加工页未选中",
                            "拍照-刚拍的照片选中检测")

            status = curr_publish_core_activity.tap_add_photo_button()
            self.assertTrue(status, "添加图片,进入图片选择页失败")

            curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)

            photo_count = curr_gallery_activity.image_photo_enable_picked_count
            curr_photo_list = curr_gallery_activity.image_photo_list
            log.logger.info("随机选1张图片")
            #  选随机选择几张图片,为了排除底部遮罩tab的干扰，图片最多选择11张
            max_pick_count = photo_count if photo_count < 11 else 11

            index = random.randint(2, max_pick_count)  # 该页面第一个格子为拍照按钮
            log.logger.info("选择相册中的第{}张照片".format(index))
            curr_photo_list[index-1].select()
            log.logger.info("验证该图片有没有被选中")
            self.assertEqual('2', curr_photo_list[index-1].check_value, "该图片没有被选中",
                             "拍照-选中已有照片检测")
            log.logger.info("该图片已被选中")

            log.logger.info("验证已选中的图片的数目")
            self.assertEqual('2', curr_gallery_activity.selected_photo_count, "选择的图片数量不一致",
                             "拍照-验证已选择照片数目")

            status = curr_gallery_activity.tap_photo_next_step_button()
            self.assertTrue(status, "进入照片加工页失败")

        except Exception as exp:
            log.logger.error("发现异常, case:test_take_and_pick_photo_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'take_and_pick_photo', exp)

    def test_publish_core_operation(self):
        """
            test_cases/test_photo_operations.py:PhotoTestCase.test_publish_core_operation
            Summary:
                选择图片-进入发布核心页-贴纸/滤镜/标签/玩字
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)

            log.logger.info("切换一次底部tab，避免\"发布故事集\"的引导遮罩对选取图片的干扰")
            curr_gallery_activity.tap_story_tab()
            curr_gallery_activity.tap_photo_tab()

            photo_count = curr_gallery_activity.image_photo_enable_picked_count
            curr_photo_list = curr_gallery_activity.image_photo_list
            log.logger.info("随机选1张图片")
            #  选随机选择几张图片,为了排除底部遮罩tab的干扰，图片最多选择11张
            max_pick_count = photo_count if photo_count < 11 else 11

            index = random.randint(1, max_pick_count)
            log.logger.info("选择相册中的第{}张照片".format(index))
            curr_photo_list[index-1].select()
            log.logger.info("验证该图片有没有被选中")
            self.assertEqual('1', curr_photo_list[index-1].check_value, "该图片没有被选中")
            log.logger.info("该图片已被选中")

            log.logger.info("验证已选中的图片的数目")
            self.assertEqual('1', curr_gallery_activity.selected_photo_count, "选择的图片数量不一致")

            curr_gallery_activity.tap_photo_next_step_button()
            curr_publish_core_activity = publish_core_activity.PublishCoreActivity(base_app)
            if curr_publish_core_activity.is_guide_mask_exist() or curr_publish_core_activity.is_sticker_mask_exist():
                log.logger.info("存在引导遮罩,移除引导遮罩")
                curr_publish_core_activity.remove_guide_mask()

            log.logger.info("验证发布加工页的图片数")
            self.assertEqual(1, len(curr_publish_core_activity.photo_available_list),
                             "发布加工页面图片数目不正确")

            # ***********进入贴纸商城检测 ***************
            log.logger.info("点击贴纸")
            status = curr_publish_core_activity.tap_paster_button()
            self.assertTrue(status, "进入贴纸商城失败", "进入贴纸商城")
            curr_paster_mall_activity = user_paster_activity.UserPasterActivity(base_app)
            curr_paster_mall_activity.tap_back_button(window=activities.ActivityNames.PUBLISH_CORE)

            # ***********滤镜检测*********************
            log.logger.info('点击滤镜')
            status = curr_publish_core_activity.tap_filter_button()
            self.assertTrue(status, "滤镜工具栏没有吊起", "滤镜工具栏吊起")

            status = curr_publish_core_activity.tap_beauty_button()
            self.assertTrue(status, "美颜强度选项没有吊起", "美颜强度栏吊起")

            level = random.randint(0, 3)
            log.logger.info("选择美颜强度级数{}".format(level))
            curr_publish_core_activity.select_beauty_level(level)

            status = curr_publish_core_activity.tap_beauty_level()
            self.assertTrue(status, "美颜强度选项没有消失", "美颜强度栏消失")

            log.logger.info('将滤镜效果栏向左边滑动')
            curr_publish_core_activity.filter_bar.swipe_left_entire_scroll_view()

            log.logger.info('选择屏幕内第二个滤镜效果')
            curr_publish_core_activity.filter_effect_choice_list[1].select()
            self.assertTrue(curr_publish_core_activity.is_seek_bar_exist(), "滤镜效果调整框不存在", "滤镜效果调整栏检测")

            curr_publish_core_activity.filter_seek_bar.slide('right', 0.75)

            log.logger.info('将滤镜效果栏向右侧滑动,露出无滤镜效果选项')
            curr_publish_core_activity.filter_bar.swipe_right_entire_scroll_view()

            while not curr_publish_core_activity.is_no_filter_effect_displayed():
                log.logger.info("无滤镜效果不在屏幕内,继续向右滑动")
                curr_publish_core_activity.filter_bar.swipe_right_entire_scroll_view()

            log.logger.info("选择无滤镜效果")
            curr_publish_core_activity.filter_effect_choice_list[0].select()
            self.assertTrue(curr_publish_core_activity.is_seek_bar_not_exist(), "滤镜效果调整框还存在", "滤镜效果栏取消检测")

            # ***********标签检测*********************
            log.logger.info('点击标签按钮,吊起标签遮罩')
            status = curr_publish_core_activity.tap_mark_tool()
            self.assertTrue(status, '吊起标签失败', "吊起标签")

            log.logger.info('点击文字标签')
            status = curr_publish_core_activity.tap_words_tag()
            self.assertTrue(status, "进入文字标签页失败", "玩字-进入文字标签页")

            curr_words_tag_activity = publish_words_tag_activity.PublishWordsTagActivity(base_app)
            curr_words_tag_activity.input_words(u'庐山升龙霸')
            curr_words_tag_activity.tap_add_button()

            self.assertTrue(curr_words_tag_activity.is_tag_added_successful(), '标签添加失败', "添加文字标签")

            # ***********玩字检测*********************
            log.logger.info("点击玩字按钮")
            status = curr_publish_core_activity.tap_character_button()
            self.assertTrue(status, '进入玩字页面失败', "进入玩字页")
            curr_words_art_activity = publish_words_art_activity.PublishWordsArtActivity(base_app)

            log.logger.info("点击风景tab")
            curr_words_art_activity.tab_bar.scenery_tab.tap()

            log.logger.info("选择第一张字点击")
            curr_words_art_activity.word_art_list[0].tap()

            status = curr_publish_core_activity.make_words_art_popup_appearance()
            self.assertTrue(status, '玩字遮罩未呼出', "吊起玩字遮罩")

            words_art_widget = bottom_popup_art_text_window.BottomPopupArtTextWindow(base_app)

            word_count = len(words_art_widget.words_available_list)

            log.logger.info("当前推荐的文字词语个数为{}".format(word_count))
            index = random.randint(0, word_count - 1)

            log.logger.info("随机选择第{}个词语".format(index + 1))
            words_art_widget.select_words_available(index)
            status = words_art_widget.words_length_check()
            self.assertTrue(status, '文字输入的字数计算错误', "玩字-选中给定字-玩字输入字数量检测")

            words_art_widget.input_words(u'中秋月圆')
            status = words_art_widget.words_length_check()
            self.assertTrue(status, '文字输入的字数计算错误', "玩字-输入自定义字-丸子输入字数检测")

            words_art_widget.tap_use_button()

            curr_publish_core_activity.tap_finish_button()

            curr_publish_activity = publish_activity.PublishActivity(base_app)
            log.logger.info("验证发布的图片数量")
            self.assertEqual(1, len(curr_publish_activity.photo_available_list), "发布贴纸数量不正确", "发布特效照片-贴纸数量检测")

            curr_publish_activity.input_words(u"测试图片发布")
            curr_publish_activity.tap_publish_button()
            log.logger.info("开始验证发布情况")
            status = curr_publish_activity.is_publish_successful()
            self.assertTrue(status, "发布失败", "发布特效照片-发布成功")

        except Exception as exp:
            log.logger.error("发现异常, case:test_publish_core_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'take_publish_core', exp)
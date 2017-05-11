#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 贴纸操作

Authors: Turinblueice(hongquan@itugo.com)
Date:    16/5/5 17:47
"""

import random

from activities.common_activities import camera2_activity
from activities.common_activities import photo_picker_activity
from activities.common_activities import story_gallery_activity
from activities.publish_activities import publish_activity
from activities.publish_activities import publish_core_activity
from activities.publish_activities import publish_words_tag_activity
from activities.user_center_sub_activities.user_paster_activites import custom_paster_crop_activity
from activities.user_center_sub_activities.user_paster_activites import custom_paster_editor_activity
from activities.user_center_sub_activities.user_paster_activites import cut_out_paster_activity
from activities.user_center_sub_activities.user_paster_activites import my_own_paster_tab_activity
from activities.user_center_sub_activities.user_paster_activites import select_photo_guide_activity
from base import devices_base_test
from base import base_frame_view
from common_actions import access_action
from gui_widgets.custom_widgets import continue_popup_window
from gui_widgets.custom_widgets import custom_paster_msgbox
from util import log


class PasterTestCase(devices_base_test.DevicesBaseTest):

    def __init__(self, *args, **kwargs):
        super(PasterTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        self.create_driver(self.debug_mode)
        driver = self.get_driver()

        action = access_action.AccessAction(driver)
        action.wait_for_app_launch(6)
        action.go_to_my_paster()  # 准备工作，进入我的贴纸页面

    def tearDown(self):
        driver = self.get_driver()
        if driver:
            driver.quit()
        self.get_current_html_reporter().finalize()

    def test_create_paster_operation(self):
        """
            test_cases/test_paster_operations.py:PasterTestCase.test_create_paster_operation
            Summary:
                创建贴纸
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_my_own_paster_tab_activity = my_own_paster_tab_activity.MyOwnPasterTabActivity(base_app)

            # 记录当前贴纸个数
            tmp_my_paster_num = len(curr_my_own_paster_tab_activity.my_custom_paster_list)
            log.logger.info("当前已有贴纸数{}张".format(tmp_my_paster_num))

            curr_my_own_paster_tab_activity.tap_add_paster_button(auto=True)

            if curr_my_own_paster_tab_activity.is_guide_exist():
                #  如果是首次添加贴纸，则进行引导页的操作
                curr_crop_activity = custom_paster_crop_activity.CustomPasterCropActivity(base_app)
                status = curr_crop_activity.tap_create_my_paster_button()
                self.assertTrue(status, "进入贴纸选择导航页失败", "创建贴纸-首次-进入贴纸引导页")

                curr_guide_photo_activity = select_photo_guide_activity.SelectPhotoGuideActivity(base_app)
                status = curr_guide_photo_activity.tap_guide_tip()
                self.assertTrue(status, "进入图片选择页失败", "创建贴纸-首次-取消引导进入图片选择页")

                curr_photo_picker_activity = photo_picker_activity.PhotoPickerActivity(base_app)
                index = 1
                curr_photo_picker_activity.select_image(index)
                status = curr_photo_picker_activity.tap_next_step_button()
                self.assertTrue(status, "进入图片区域选择页失败", "创建贴纸-首次-进入图片选择页")

                status = curr_crop_activity.tap_continue_button()
                self.assertTrue(status, "进入图片剪切页失败", "创建贴纸-首次-进入图片剪切页")

                log.logger.info("点击一次屏幕中心，取消图片剪切页的引导遮罩")
                base_app.tap_window_center()

                curr_cut_out_activity = cut_out_paster_activity.CutOutPasterActivity(base_app)
                status = curr_cut_out_activity.tap_continue_button()
                self.assertTrue(status, "进入贴纸搭配页失败", "创建贴纸-首次-进入贴纸搭配页")

                log.logger.info("点击一下屏幕中心，取消贴纸搭配页的引导遮罩")
                base_app.tap_window_center()
            else:
                # 非首次点击添加贴纸，则从底部吊起贴纸添加选择面板
                index = 2
                log.logger.info("吊起添加贴纸面板,选择第{}张贴纸作为模板".format(index))
                status = curr_my_own_paster_tab_activity.select_paster_available(index)
                self.assertTrue(status, "进入贴纸搭配页失败", "非首次-进入贴纸搭配页")

            curr_paster_editor_activity = custom_paster_editor_activity.CustomPasterEditorActivity(base_app)
            status = curr_paster_editor_activity.tap_continue_button()
            self.assertTrue(status, "创建贴纸失败", "创建贴纸")

            log.logger.info("验证创建的贴纸添加到了已有贴纸里面")
            now_my_paster_num = len(curr_my_own_paster_tab_activity.my_custom_paster_list)
            log.logger.info("现在贴纸数目{}张".format(now_my_paster_num))

            self.assertEqual(1, now_my_paster_num-tmp_my_paster_num, "贴纸数量不一致，创建贴纸失败", "创建后,贴纸数目检测")

        except Exception as exp:
            log.logger.error("发现异常, case:test_paster_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'create_paster', exp)

    def test_publish_paster_available_operation(self):
        """
            test_cases/test_paster_operations.py:PasterTestCase.test_publish_paster_available_operation
            Summary:
                发布已有贴纸
        """
        base_app = base_frame_view.BaseFrameView(self.get_driver())
        try:
            curr_my_own_paster_tab_activity = my_own_paster_tab_activity.MyOwnPasterTabActivity(base_app)

            # 记录当前贴纸个数
            tmp_my_paster_num = len(curr_my_own_paster_tab_activity.my_custom_paster_list)
            log.logger.info("当前已有贴纸数{}张".format(tmp_my_paster_num))

            index = random.randint(1, tmp_my_paster_num-1)
            log.logger.info("点击第{}张贴纸".format(index))
            status = curr_my_own_paster_tab_activity.choose_custom_paster(index)
            self.assertTrue(status, "吊起贴纸对话框失败", "发布已有贴纸-吊起贴纸对话框")

            curr_paster_box = custom_paster_msgbox.CustomPasterMsgBox(base_app)
            status = curr_paster_box.tap_use_button()
            self.assertTrue(status, "使用贴纸失败", "发布已有贴纸-使用贴纸")

            curr_camera2_activity = camera2_activity.Camera2Activity(base_app)

            if curr_camera2_activity.is_continue_popup_exist():
                log.logger.info("存在\"是否保留上次贴纸\"的提示遮罩")
                popup_window = continue_popup_window.ContinuePopupWindow(base_app)
                log.logger.info("点击新建按钮")
                popup_window.tap_new_button()

            status = curr_camera2_activity.tap_camera()
            self.assertTrue(status, '贴纸确定失败', '使用贴纸-贴纸拍照')

            log.logger.info("确认贴纸")
            status = curr_camera2_activity.tap_finish_camera()
            self.assertTrue(status, "进入贴纸发布加工页失败")

            curr_publish_core_activity = publish_core_activity.PublishCoreActivity(base_app)
            if curr_publish_core_activity.is_guide_mask_exist() or curr_publish_core_activity.is_sticker_mask_exist():
                curr_publish_core_activity.tap_window_center()

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

            self.assertTrue(curr_words_tag_activity.is_tag_added_successful(), '标签添加失败', "发布贴纸-添加文字标签")

            log.logger.info("添加图片到发布贴纸")
            curr_publish_core_activity.tap_add_photo_button()

            log.logger.info("选择图片，编辑贴纸")
            curr_story_gallery_activity = story_gallery_activity.StoryGalleryActivity(base_app)
            indexes = (3, 2, 4)

            for index, value in enumerate(indexes, start=1):
                curr_story_gallery_activity.select_image_photo(value)
                self.assertEqual(str(index+1), curr_story_gallery_activity.image_photo_list[value-1].check_value,
                                 "选中序号不正确", "发布已有贴纸-第{}张图的序号{}检测".format(value, index))

            log.logger.info("验证总贴纸数")
            self.assertEqual('4', curr_story_gallery_activity.selected_photo_count, "选择的贴纸总数不正确",
                             "发布已有贴纸-增加贴纸数检测")  # 拍照+选择3张共4张

            status = curr_story_gallery_activity.tap_photo_next_step_button()
            self.assertTrue(status, "进入发布加工页失败")
            
            if curr_publish_core_activity.is_guide_mask_exist() or curr_publish_core_activity.is_sticker_mask_exist():
                curr_publish_core_activity.tap_window_center()

            self.assertEqual(len(indexes)+1, len(curr_publish_core_activity.photo_available_list), "发布贴纸数量不正确",
                             "发布贴纸-发布加工页-验证贴纸图片数")

            status = curr_publish_core_activity.tap_finish_button()
            self.assertTrue(status, "进入发布页失败", "发布已有贴纸-进入发布页")
            curr_publish_activity = publish_activity.PublishActivity(base_app)
            log.logger.info("验证发布的图片数量")
            self.assertEqual(len(indexes)+1, len(curr_publish_activity.photo_available_list), "发布贴纸数量不正确",
                             "发布页-发布页验证贴纸图片数")

            curr_publish_activity.input_words(u"测试发布")
            curr_publish_activity.tap_publish_button()
            log.logger.info("开始验证发布情况")
            status = curr_publish_activity.is_publish_successful()
            self.assertTrue(status, "发布失败", "发布已有贴纸")

        except Exception as exp:
            log.logger.error("发现异常, case:test_publish_paster_available_operation执行失败")
            self.raise_exp_and_save_screen_shot(base_app, 'test_publish_paster', exp)
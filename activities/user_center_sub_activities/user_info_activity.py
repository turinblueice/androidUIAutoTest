#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-编辑资料

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.custom_widgets import alert

from activities.common_activities import photo_picker_activity
from activities.common_activities import cropper_image_activity

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from activities import activities

import time
import random


class UserInfoActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-编辑资料

        Attributes:

    """
    name = '.usercenter.activity.EditInfoActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(UserInfoActivity, self).__init__(parent)
        self._scroll_view = scroll_view.ScrollView(self.parent, type='android.widget.ScrollView')

    @property
    def title(self):
        """
            Summary:
                标题-编辑资料
        """
        id_ = "com.jiuyan.infashion:id/editinfo_tv_title"
        return text_view.TextView(self.parent, id=id_).text

    @property
    def back_button(self):
        """
            Summary:
                后退按钮
        """
        id_ = "com.jiuyan.infashion:id/editinfo_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def complete_button(self):
        """
            Summary:
                完成按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/editinfo_btn_complete'
        return button.Button(self.parent, id=id_)

    @property
    def avatar_bar(self):
        """
            Summary:
                头像栏
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_editinfo_rl_avater'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def nickname_edit_box(self):
        """
            Summary:
                昵称修改文本输入框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_editinfo_et_nickname'
        return edit_text.EditText(self._scroll_view, id=id_)

    @property
    def in_id_edit_box(self):
        """
            Summary:
                in号输入框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_editinfo_et_inNumber'
        return edit_text.EditText(self._scroll_view, id=id_)

    @property
    def region_bar(self):
        """
            Summary:
                地区栏
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_editinfo_rl_address'
        return relative_layout.RelativeLayout(self._scroll_view, id=id_)

    @property
    def region_text(self):
        """
            Summary:
                地区的显示文本
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/usercenter_editinfo_tv_address'
        return text_view.TextView(self._scroll_view, id=id_).text

    # ************************操作***************************
    def upload_avatar(self):
        """
            Summary:
                上传头像
        """
        log.logger.info("点击头像栏")
        self.avatar_bar.tap()
        if self.wait_activity(activities.ActivityNames.PHOTO_PICKER, 10):
            log.logger.info("已进入图片上传活动页")
            curr_photo_picker_activity = photo_picker_activity.PhotoPickerActivity(self.parent)
            log.logger.info("随机上传一张照片作为头像")
            index = random.randint(0, len(curr_photo_picker_activity.post_image_list)-1)
            curr_photo_picker_activity.select_image(index)
            if curr_photo_picker_activity.tap_next_step_button():
                log.logger.info("已经进入编辑图片活动页")
                curr_cropper_activity = cropper_image_activity.CropperImageActivity(self.parent)
                if curr_cropper_activity.tap_ok_button():
                    log.logger.info("已成功上传头像")
                    return True
        log.logger.error("上传头像失败")
        return False

    def edit_nickname(self, *values):
        """
            Summary:
                编辑昵称
        """
        log.logger.info("开始编辑昵称")
        self.nickname_edit_box.clear_text_field()
        self.nickname_edit_box.send_keys(*values)
        time.sleep(1)
        log.logger.info("编辑昵称完毕")

    def edit_in_id(self, *values):
        """
            Summary:
                编辑id
            Args:
                values: 元组，编辑的值
        """
        log.logger.info("开始编辑in号")
        self.in_id_edit_box.clear_text_field()
        self.in_id_edit_box.send_keys(*values)
        time.sleep(1)
        log.logger.info("编辑in号完毕")

    def select_region(self, city):
        """
            Summary:
                选择地区-城市
            Args:
                city: 城市名称
        """
        log.logger.info("点击地区栏")
        self.region_bar.tap()
        log.logger.info("等待对话框弹出")
        WebDriverWait(self.base_parent, 10).until(
            EC.text_to_be_present_in_element((MobileBy.ID, 'android:id/alertTitle'), alert.SelectCityAlert.title_value)
        )
        curr_alert = alert.SelectCityAlert(self.base_parent)

        if hasattr(curr_alert, 'select_'+city):
            getattr(curr_alert, 'select_'+city)()
            log.logger.info("点击确定按钮")
            curr_alert.confirm_button.tap()
            log.logger.info("城市选择完毕")
        else:
            log.logger.error('该城市：{}输入错误，无法到达'.format(city))
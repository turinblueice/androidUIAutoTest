#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 他人in记更改资料页面

Authors: Turinblueice
Date: 2016/7/26
"""

from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import checked_text_view
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import scroll_view

from appium.webdriver import WebElement

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from activities import activities
from selenium.common.exceptions import TimeoutException
from devices_manager import command_prompt

import time


class PersonalRemarkActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        他人in记更改资料页面

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.usercenter.activity.UserCenterReMarkActicity'

    def __init__(self, parent):
        super(PersonalRemarkActivity, self).__init__(parent)

        self._scroll_view = scroll_view.ScrollView(
            self.parent, type='android.widget.ScrollView')

    # *****************************更改页头部属性********************************
    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_usercenter_setting_back'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def complete_button(self):
        """
            Summary:
                完成按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_usercenter_setting_right'
        return text_view.TextView(self.parent, id=id_)

    @property
    def avatar(self):
        """
            Summary:
                头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def remark_username(self):
        """
            Summary:
                备注名
        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_username'
        return text_view.TextView(self.parent, id=id_)

    @property
    def more_button(self):
        """
            Summary:
                详细资料
        """
        id_ = 'com.jiuyan.infashion:id/remark_more_tv'
        return text_view.TextView(self.parent, id=id_)

    # ****************************更改属性**************************************
    @property
    def friends_check(self):
        """
            Summary:
                将他关注为朋友的checkbox
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_sort_friends'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def interest_check(self):
        """
            Summary:
                将他关注为订阅的checkbox
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_sort_interest'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def remark_edit_box(self):
        """
            Summary:
                备注名编辑框
        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_name_et'
        return edit_text.EditText(self.parent, id=id_)

    # ******************************最下方三栏**********************************

    @property
    def share_bar(self):
        """
            Summary:
                把他推荐给好友栏
        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_share_ll'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def report_bar(self):
        """
            Summary:
                 举报栏
        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_report_ll'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def black_list_switch(self):
        """
            Summary:
                 加入黑名单开关
        """
        id_ = 'com.jiuyan.infashion:id/uc_remark_black_checktext'
        return checked_text_view.CheckedTextView(self.parent, id=id_)

    @property
    def black_dialogue(self):
        """
            Summary:
                加入黑名单对话框
        Returns:

        """
        id_ = 'android:id/content'
        return BlackDialogue(self.parent, id=id_)

    # ***********************操作方法*********************************

    def tap_back_button(self):
        """
            Summary:
                点击后退按钮
        """
        log.logger.info("开始点击后退按钮")
        self.back_button.tap()
        log.logger.info("结束后退按钮点击")
        if self.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功回到个人in记主页面")
            return True
        log.logger.info("回到个人in记主页面失败")
        return False

    def tap_ok_button(self):
        """
            Summary:
                点击后退按钮
        """
        log.logger.info("开始点击完成按钮")
        self.complete_button.tap()
        log.logger.info("结束完成按钮点击")
        if self.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功回到个人in记主页面")
            return True
        log.logger.info("回到个人in记主页面失败")
        return False

    def tap_avatar(self):
        """
            Summary:
                点击头像
        """
        log.logger.info("开始点击后退按钮")
        self.avatar.tap()
        log.logger.info("结束后退按钮点击")
        if self.wait_activity(activities.ActivityNames.BIG_HEAD, 10):
            log.logger.info("成功回到头像详情页")
            return True
        log.logger.info("回到头像详情页失败")
        return False

    def select_group(self, group_name='friends'):
        """

        Args:
            group_name: 两个值friend表示勾选朋友,interest表示勾选订阅

        Returns:

        """
        words = {'friends': '朋友', 'interest': '订阅'}

        if group_name in ('friends', 'interest'):
            log.logger.info("开始点击\"{}\"分组".format(words[group_name]))
            getattr(self, group_name+'_check', None).tap()
            log.logger.info("点击完毕")
            log.logger.info("检查是否已选中\"{}\"分组".format(words[group_name]))
            try:
                WebDriverWait(self.base_parent, 3).until(
                    EC.element_located_to_be_selected(
                        (MobileBy.ID, 'com.jiuyan.infashion:id/uc_remark_sort_{}'.format(group_name)))
                )
                log.logger.info("已选中\"{}\"分组".format(words[group_name]))
                return True
            except:
                log.logger.error("选择\"{}\"分组失败".format(words[group_name]))
                return False
        else:
            log.logger.error("group_name值错误,只能选择friends或者interest")
            return False

    def input_remark_name(self, *values):
        """
            Summary:
                更改备注名
        Args:
            *values:

        Returns:

        """
        log.logger.info("清空输入框")
        self.remark_edit_box.clear_text_field()
        log.logger.info("开始输入备注名")
        self.remark_edit_box.send_keys(*values)
        log.logger.info("完成输入")
        time.sleep(2)

    def tap_blacklist_switch(self, open_switch=True):
        """
            Summary:
                打开黑名单开关
            Args:
                open_switch:True:加入黑名单;False:取消黑名单

        """
        log.logger.info("点击黑名单按钮")
        self.black_list_switch.tap()
        log.logger.info("黑名单点击完毕")
        if open_switch:
            log.logger.info("加入黑名单")
            if self.wait_for_element_present(self.base_parent,
                                             id='com.jiuyan.infashion:id/dialog_blacklist_cancel', timeout=3):
                log.logger.info("成功调出提示框")
                curr_dialogue = BlackDialogue(self.parent)
                log.logger.info("点击提示框确定按钮")
                curr_dialogue.tap_ok_button()
                log.logger.info("完成确定按钮点击")
                return True
            log.logger.error("黑名单提示框弹出失败")
            return False
        else:
            log.logger.info("取消黑名单")
            return True


class BlackDialogue(base_frame_view.BaseFrameView):
    """
        Summary:
            拉黑对话框
    """

    def __init__(self, parent, **kwargs):
        super(BlackDialogue, self).__init__(parent)
        self._dialogue = self.find_element(**kwargs)

    @property
    def title(self):
        """
            Summary:
                标题
        Returns:

        """

        return text_view.TextView(self._dialogue, type='android.widget.TextView').text

    @property
    def friend_group(self):
        """
            Summary:
                朋友分组
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_chose_friend_type_ll_friend'
        return linear_layout.LinearLayout(self._dialogue, id=id_)

    @property
    def ok_button(self):
        """
            Summary:
                确定按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_blacklist_sure'
        return text_view.TextView(self._dialogue, id=id_)

    @property
    def cancel_button(self):
        """
            Summary:
                取消按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_blacklist_cancel'
        return text_view.TextView(self._dialogue, id=id_)

    # ********************操作方法*******************

    def tap_ok_button(self):
        """
            Summary:
                点击完成按钮
        Returns:

        """
        log.logger.info("开始点击完成按钮")
        self.ok_button.tap()
        log.logger.info("完成点击")
        time.sleep(2)

    def tap_cancel_button(self):
        """
            Summary:
                点击取消按钮
        Returns:

        """
        log.logger.info("开始点击取消按钮")
        self.cancel_button.tap()
        log.logger.info("完成点击")
        time.sleep(2)



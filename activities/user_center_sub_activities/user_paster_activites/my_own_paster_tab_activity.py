#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-我的贴纸-我的tab

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.basic_widgets import view_pager

from gui_widgets.custom_widgets import search_bar
from activities import activities
from activities.user_center_sub_activities.user_paster_activites import user_paster_activity

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


class MyOwnPasterTabActivity(user_paster_activity.UserPasterActivity):

    """
        Summary:
            用户中心-我的贴纸-我的tab页

        Attributes:

    """
    name = '.module.paster.activity.PasterMallActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(MyOwnPasterTabActivity, self).__init__(parent)
        self.__scroll_view = scroll_view.ScrollView(self.parent, id='com.jiuyan.infashion:id/scroll')

    @property
    def add_paseter_button(self):
        """
            Summary:
                添加贴纸按按钮
        """
        view_pager_ = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/cp_pager')

        # id为cp_pager的view_pager的第一个layout_root元素为添加贴纸按钮
        return frame_layout.FrameLayout(view_pager_, id='com.jiuyan.infashion:id/layout_root')

    @property
    def add_template_button(self):
        """
            Summary:
                添加模板按钮
        """
        view_pager_ = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/playtips_pager')

        # id为playtips_pager的view_pager的第一个layout_root元素为添加模板按钮
        return frame_layout.FrameLayout(view_pager_, id='com.jiuyan.infashion:id/layout_root')

    @property
    def used_recently_paster_list(self):
        """
            Summary:
                最近使用贴纸列表
        :return:
        """
        view_pager_element = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/history_pager')

        return frame_layout.FrameLayoutList(view_pager_element, type='android.widget.FrameLayout')

    @property
    def my_custom_paster_list(self):
        """
            Summary:
                我的自定义贴纸列表
        """
        view_pager_element = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/cp_pager')
        # view_pager_element.wait_for_element_present(type='android.widget.FrameLayout')
        # 第一个元素为按钮，移出列表
        return frame_layout.FrameLayoutList(view_pager_element, type='android.widget.FrameLayout').frame_list[1:]

    @property
    def my_keep_template_list(self):
        """
            Summary:
                收藏的模板列表
        :return:
        """
        view_pager_element = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/playtips_pager')

        return frame_layout.FrameLayoutList(view_pager_element, type='android.widget.FrameLayout').frame_list[1:]

    # ************************选择贴纸模板遮罩**********************

    @property
    def paster_available_list(self):
        """
            Summary:
                已有贴纸列表
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[1]/android.widget.RelativeLayout'
        return relative_layout.RelativeLayoutList(self.parent, xpath=xpath_).relative_layout_list

    @property
    def select_from_gallery_button(self):
        """
            Summary:
                从手机相册中选择按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/select_gallery'
        return text_view.TextView(self.parent, id=id_)

    @property
    def cancel_popup_button(self):
        """
            Summary:
                取消弹层按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/cancle'
        return text_view.TextView(self.parent, id=id_)

    # ************************操作方法***************************
    def choose_custom_paster(self, index):
        """
            Summary:
                在自定义贴纸列表中，选择已有自定义贴纸
            Args:
                index: 序号
        :return:
        """
        log.logger.info("开始选择第{}张贴纸".format(index))
        self.my_custom_paster_list[index-1].tap()
        log.logger.info("完成第{}张贴纸点击".format(index))
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.presence_of_element_located((MobileBy.ID, 'com.jiuyan.infashion:id/tv_dialog_sticker_name')))
            log.logger.info("已吊起贴纸对话框")
            return True
        except TimeoutException:
            log.logger.info("吊起贴纸对话框失败")
            return False

    def is_guide_exist(self):
        """
            Summary:
                是否出现添加贴纸的引导页
        :return:
        """
        try:
            if self.current_activity == activities.ActivityNames.CUSTOM_PASTER_CROP:
                WebDriverWait(self.base_parent, 10).until(
                    EC.presence_of_element_located(
                        (MobileBy.ID, 'com.jiuyan.infashion:id/btn_guide_ok')
                    )
                )
                return True
            return False
        except TimeoutException:
            return False

    def tap_add_paster_button(self, auto=True, is_first=False):
        """
            Summary:
                点击添加贴纸按钮
            auto: True:自动识别是否是首次点击，如果是首次，则直接进入引导流程
        """
        log.logger.info("点击添加贴纸按钮")
        time.sleep(2)
        self.add_paseter_button.tap()
        log.logger.info("完成贴纸添加按钮的点击")
        if auto:
            if self.wait_activity(activities.ActivityNames.CUSTOM_PASTER_CROP, 5):
                #  判断是否首次点击，首次则会进入引导页
                log.logger.info("首次点击添加贴纸")
                log.logger.info("成功进入贴纸创建引导页")
                return True

            else:
                log.logger.info("非首次点击添加贴纸")
                try:
                    WebDriverWait(self.base_parent, 10).until(
                        EC.presence_of_element_located(
                            (MobileBy.XPATH,
                             '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/recycler"]'))
                    )
                    log.logger.info("成功吊起添加贴纸的面板")
                    return True
                except TimeoutException:
                    log.logger.error("吊起添加贴纸面板失败")
                    return False
        else:
            if is_first:
                log.logger.info("首次点击添加贴纸")
                if self.wait_acitivity(activities.ActivityNames.CUSTOM_PASTER_CROP, 10):
                    log.logger.info("成功进入添加图片的引导页")
                    return True
                log.logger.error("未进入添加图片的引导页")
                return False
            else:
                log.logger.info("吊起贴纸添加面板")
                try:
                    WebDriverWait(self.base_parent, 10).until(
                        EC.presence_of_element_located(
                            (MobileBy.XPATH,
                             '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/recycler"]'))
                    )
                    log.logger.info("成功吊起添加贴纸的面板")
                    return True
                except TimeoutException:
                    log.logger.error("吊起添加贴纸面板失败")
                    return False

    def select_paster_available(self, index):
        """
            Summary:
                在弹出的popupwindow里面选择贴纸
            Args:
                index：贴纸序号
        """
        log.logger.info("开始选择第{}张贴纸".format(index))
        self.paster_available_list[index-1].tap()
        if self.wait_activity(activities.ActivityNames.CUSTOM_PASTER_EDITOR, 10):
            log.logger.info("成功进入贴纸搭配页")
            return True
        log.logger.info("进入贴纸搭配页失败")
        return False

    def select_from_gallery(self):
        """
            Summary:
                从相册中选择
        :return:
        """
        log.logger.info("点击从相册中选择按钮")
        self.select_from_gallery_button.tap()
        log.logger.info("完成从相册中选择按钮的点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_PICKER, 10):
            log.logger.info("成功进入图片选择页")
            return True
        log.logger.error("进入图片选择页失败")
        return False

    def tap_cancel_popup(self):
        """
            Summary:
                点击取消弹出面板按钮
        :return:
        """
        log.logger.info("点击取消按钮")
        self.cancel_popup_button.tap()
        log.logger.info("点击结束")
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.presence_of_element_located((MobileBy.XPATH, '//android.widget.TextView[@text="我的"]'))
            )
            return True
        except TimeoutException:
            return False

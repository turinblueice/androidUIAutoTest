#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-我的好友

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
from gui_widgets.basic_widgets import list_view
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.custom_widgets import alert

from activities.common_activities import photo_picker_activity
from activities.common_activities import cropper_image_activity

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver import WebElement
from activities import activities

import time


class UserFriendsActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-我的好友

        Attributes:

    """
    name = '.usercenter.activity.UserCenterFriendsActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(UserFriendsActivity, self).__init__(parent)

    @property
    def back_button(self):
        """
            Summary:
                后退按钮
        """
        id_ = "com.jiuyan.infashion:id/uc_friend_iv_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def search_box_button(self):
        """
            Summary:
                搜索框按钮
        """
        id_ = 'com.jiuyan.infashion:id/uc_search_main_friends_ll'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def search_edit_box(self):
        """
            Summary:
                搜索输入框
        """
        id_ = 'com.jiuyan.infashion:id/uc_cet_search_friends2'
        return edit_text.EditText(self.parent, id=id_)

    @property
    def friend_item_list(self):
        """
            Summary:
                好友搜索结果列表
        """
        xpath_ = '//android.widget.ListView[@resource-id=\"com.jiuyan.infashion:id/uc_lv_add_friends\"]/' \
                 'android.widget.LinearLayout'

        return FriendItemList(self.parent, xpath=xpath_).item_list

    #  *************************操作方法**************************
    def check_friend_in_search_list(self, name):
        """
            Summary:
                检查好友名称是否在搜索结果列表中
        """
        friend_list = self.friend_item_list
        for index, friend in enumerate(friend_list, start=1):
            if name == friend.friend_name:
                log.logger.info("第{}条搜索结果为检索好友结果".format(index))
                return index
        return False

    def display_search_list(self):
        """
            Summary:
                点击搜索，展示搜索结果列表
        :return:
        """
        log.logger.info("点击搜索框按钮，激活搜索框")
        self.search_box_button.tap()
        if self.wait_for_element_present(self.base_parent, id='com.jiuyan.infashion:id/uc_cet_search_friends2'):
            self.search_edit_box.clear_text_field()
            log.logger.info("输入空格呼出检索结果")

            for index in range(3):
                log.logger.info("第{}次输入".format(index+1))
                self.search_edit_box.send_keys(' ')
                time.sleep(2)
                if self.wait_for_element_present(
                        self.base_parent,
                        xpath='//android.widget.ListView[@resource-id=\"com.jiuyan.infashion:id/uc_lv_add_friends\"]'):
                    log.logger.info("已成功呼出搜索结果列表")
                    return True
            log.logger.error("搜索结果列表没有呼出")
            return False
        raise TimeoutException('搜索输入框未及时出现')

    def search_friend(self, *values):
        """
            Summary:
                搜索朋友
            Args:
                values: 搜索词
        """
        log.logger.info("点击搜索框按钮，激活搜索框")
        self.search_box_button.tap()
        if self.wait_for_element_present(self.base_parent, id='com.jiuyan.infashion:id/uc_cet_search_friends2'):
            log.logger.info("开始输入搜索词")
            self.search_edit_box.clear_text_field()
            self.search_edit_box.send_keys(*values)
            time.sleep(2)
            self.base_parent.keyevent(66)  # 发送键盘回车事件
            log.logger.info("输入完毕")
            return True
        raise TimeoutException('搜索输入框未及时出现')

    def is_search_result_exist(self):
        """
            Summary:
                是否存在搜索结果
        """
        list_view_ = list_view.ListView(self.parent, type='android.widget.ListView')
        if self.wait_for_element_present(list_view_, type='android.widget.LinearLayout'):
            return True
        return False


class FriendItem(base_frame_view.BaseFrameView):
    """
        Summary:
            好友item
    """
    def __init__(self, parent, item=None, **kwargs):
        super(FriendItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def friend_name(self):
        """
            Summary:
                好友名称
        """
        id_ = 'com.jiuyan.infashion:id/uc_new_friend_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def friend_source(self):
        """
            Summary:
                好友来源
        """
        id_ = 'com.jiuyan.infashion:id/uc_new_friend_source'
        return text_view.TextView(self._layout_view, id=id_).text

    #  ******************************操作方法********************************

    def tap(self):
        """
            Summary:
                点击该好友item去到好友主页
        """
        log.logger.info("开始点击该朋友item")
        self._layout_view.click()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入日记主页")
            return True
        log.logger.error("进入日记主页失败")
        return False


class FriendItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(FriendItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [FriendItem(item.parent, item) for item in self.__list]
        return None
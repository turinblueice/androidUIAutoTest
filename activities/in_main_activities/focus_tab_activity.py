#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: IN主页-关注tab页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import edit_text

from gui_widgets.custom_widgets import send_comment_widget

from activities import activities

from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


class FocusTabActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            In主页面-关注tab

        Attributes:

    """
    name = '.InActivity'

    def __init__(self, parent):
        super(FocusTabActivity, self).__init__(parent)
        #  等待页面网络请求进行初始化

        if self.wait_for_element_present(self.parent, timeout=10, id='com.jiuyan.infashion:id/in_title_bar'):
            self._scroll_view = recycler_view.RecyclerView(self.parent,
                                                           id='com.jiuyan.infashion:id/rv_attention_main_listview')
        else:
            log.logger.error('关注页初始化超时')
            raise

    @property
    def in_title_bar(self):
        """
            Summary:
                标题栏
        """
        id_ = 'com.jiuyan.infashion:id/in_title_bar'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def new_friend_attention_button(self):
        """
            Summary:
                新增朋友提醒按钮
        """
        id_ = 'com.jiuyan.infashion:id/msg_attention_friend'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def contact_friends_close_button(self):
        """
            Summary:
                通讯录好友提示关闭按钮
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches("com.jiuyan.infashion:id/attention_maybe_know_.*_no_data_close")'
        return image_view.ImageView(self.parent, uiautomator=uiautomator_)

    @property
    def drop_list_button(self):
        """
            Summary:
                下拉标题
        """
        id_ = "com.jiuyan.infashion:id/tv_attention_tab_current"
        return text_view.TextView(self.parent, id=id_)

    @property
    def friends_only_view(self):
        """
            Summary:
                只看朋友
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/ll_pop_menu_item'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def interest_only_view(self):
        """
            Summary:
                只看订阅
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/ll_pop_menu_item'
        return linear_layout.LinearLayoutList(self.parent, id=id_).layout_list[1]

    @property
    def drop_list_title(self):
        """
            Summary:
                下拉列表标题
        """
        id_ = "com.jiuyan.infashion:id/tv_attention_tab_current"
        return text_view.TextView(self.parent, id=id_).text

    @property
    def add_friend_button(self):
        """
            Summary:
                新增朋友按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_attention_friend_add'
        return image_view.ImageView(self.parent, id=id_)

    #**************************点击评论按钮,出现的文本框等控件*****************************

    @property
    def send_words_box(self):

        return send_comment_widget.SendCommentWidget(self.base_parent)

    # **************************用户动态卡片*****************************

    @property
    def card_list(self):

        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/rv_attention_main_listview\"]/' \
                 'android.widget.FrameLayout'

        return UserDynamicsCardList(self.base_parent, xpath=xpath_).card_list

    # ************************操作***************************
    def is_friend_attention_exist(self):
        """
            Summary:
                新增好友提醒是否存在
        :return:
        """
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/msg_attention_friend'):
            return True
        return False

    def is_contact_friends_exisit(self):
        """
            Summary:
                通讯录/微博好友提示遮罩是否存在
        Returns:

        """
        if self.wait_for_element_present(self.parent, timeout=3,
                                         uiautomator='new UiSelector().resourceIdMatches("com.jiuyan.infashion:id/attention_maybe_know_.*_no_data_close")'):
            log.logger.info("通讯录好友联系提示遮罩存在")
            return True

        log.logger.info("好友联系提示遮罩不存在")
        return False

    def tap_close_contact_button(self):
        """
            Summary:
                点击关闭好友联系button
        Returns:

        """
        log.logger.info("开始点击好友联系提示遮罩关闭按钮")
        self.contact_friends_close_button.tap()
        time.sleep(2)
        log.logger.info("点击完毕")

    def tap_drop_list_button(self, timeout=10):
        """
            Summary:
                点击下拉列表
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击下拉列表")
        self.drop_list_button.tap()
        log.logger.info("完成下拉列表的点击")
        time.sleep(timeout)

    def select_drop_item(self, index=1):
        """
            Summary:
                选择下拉列表选项
            Args:
                index： 下拉列表序号，1,2
        """
        title_bar = self.in_title_bar
        start_x = title_bar.location['x'] + title_bar.size['width']/2
        start_y = title_bar.location['y'] + title_bar.size['height']/2 + 3

        log.logger.info("开始点击第{}个列表选项")
        #  根据像素坐标点击
        self.base_parent.tap([(start_x, start_y+title_bar['height']*index)])
        log.logger.info("已经完成点击")
        time.sleep(3)

    def tap_add_friend_button(self, timeout=10):
        """
            Summary:
                点击添加朋友按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击添加朋友按钮")
        self.add_friend_button.tap()
        if self.wait_activity(activities.ActivityNames.ADD_FRIEND, timeout):
            log.logger.info("成功进入添加好友页")
            return True
        else:
            log.logger.error("进入添加还有页失败")
            return False

    #   重写向上滑动
    def swipe_up_entire_scroll_view(self, x=None):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = x or location['x'] + size['width']/3
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")
        time.sleep(2)


class UserDynamicsCard(base_frame_view.BaseFrameView):
    """
        Summary:
            用户动态卡片类
    """
    def __init__(self, parent, card=None, **kwargs):
        super(UserDynamicsCard, self).__init__(parent)
        self._layout_view = card if isinstance(card, WebElement) else self.find_element(**kwargs)

    @property
    def user_card_header_bar(self):
        """
            Summary:
                用户卡片头栏
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/friend_card_item_user_info_bar'
        return relative_layout.RelativeLayout(self._layout_view, id=id_)

    @property
    def user_avatar(self):
        """
            Summary:
                用户头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def name(self):
        """
            Summary:
                用户名称
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/friend_card_item_user_info_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def photo(self):
        """
            Summary:
                图片
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def zan_button(self):
        """
            Summary:
                点赞按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/friend_card_item_user_op_content_fav'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def comment_button(self):
        """
            Summary:
                评论按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/friend_card_item_user_op_content_recomment'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def share_button(self):
        """
            Summary:
                分享按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/friend_card_item_user_op_content_more'
        return image_view.ImageView(self._layout_view, id=id_)

    #***************发表评论后显示的评论内容******************
    @property
    def comment_list(self):
        """
            Summary:
                评论内容列表
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches(\"com.jiuyan.infashion:id/tv_comment\d*\")'
        return text_view.TextViewList(self._layout_view, uiautomator=uiautomator_).text_view_list

    @property
    def comment_user_list(self):
        """
            Summary:
                评论人列表
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches(\"com.jiuyan.infashion:id/tv_comment_user\d*\")'
        return text_view.TextViewList(self._layout_view, uiautomator=uiautomator_).text_view_list

    # **********************操作方法************************
    def tap_header_bar(self):
        """
            Summary:
                点击头栏
        Returns:

        """
        log.logger.info("开始点击头栏")
        self.user_card_header_bar.tap()
        log.logger.info("完成头栏点击")
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_DETAIL, 10):
            log.logger.info("成功进入好友图片详情页")
            return True
        log.logger.error("进入好友图片详情页失败")
        return False

    def tap_avatar(self):
        """
            Summary:
                点击头像
        Returns:

        """
        log.logger.info("开始点击头像")
        self.user_avatar.tap()
        log.logger.info("完成头像点击")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入个人信息in记页")
            return True
        log.logger.error("进入个人信息in记页失败")
        return False

    def tap_photo(self):
        """
            Summary:
                点击图片
        Returns:

        """
        log.logger.info("开始点击图片")
        self.photo.tap()
        log.logger.info("完成图片点击")
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_VIEW, 10):
            log.logger.info("成功进入图片页")
            return True
        log.logger.error("进入图片页失败")
        return False

    def tap_zan(self):
        """
            Summary:
                点赞
        Returns:

        """
        log.logger.info("开始点赞")
        self.zan_button.tap()
        log.logger.info("点赞完毕")
        try:
            #  点赞按钮被选中
            WebDriverWait(self.base_parent, 10).until(
                EC.element_located_to_be_selected((
                    MobileBy.ID, 'com.jiuyan.infashion:id/friend_card_item_user_op_content_fav'
                ))
            )

            if self.wait_for_element_present(id='com.jiuyan.infashion:id/layout_like_users'):
                log.logger.info("存在点赞人群头像组")
                return True
            log.logger.error("不存在点赞人群头像组")
            return False
        except TimeoutException:
            log.logger.error("点赞按钮没选中")
            return False

    def remove_zan(self):
        """
            Summary:
                取消点赞
        Returns:

        """
        log.logger.info("取消点赞")
        self.zan_button.tap()
        log.logger.info("取消点赞完毕")
        try:
            time.sleep(3)
            #  点赞按钮被选中
            WebDriverWait(self.base_parent, 2).until(
                EC.element_located_to_be_selected((
                    MobileBy.ID, 'com.jiuyan.infashion:id/friend_card_item_user_op_content_fav'
                ))
            )
            log.logger.error("点赞按钮依然选中")
            return False
        except TimeoutException:
            log.logger.info("点赞按钮没选中")
            return True

    def tap_comment(self):
        """
            Summary:
                点击评论
        Returns:

        """
        log.logger.info("开始点击评论")
        self.comment_button.tap()
        log.logger.info("完成评论按钮点击")
        time.sleep(3)


class UserDynamicsCardList(base_frame_view.BaseFrameView):
    """
        Summary:
            用户动态卡片类列表
    """
    def __init__(self, parent, **kwargs):
        super(UserDynamicsCardList, self).__init__(parent)
        self._card_list = self.find_elements(**kwargs)

    @property
    def card_list(self):

        if self._card_list:
            return [UserDynamicsCard(card.parent, card) for card in self._card_list]
        return None

#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 个人资料/in记主页

Authors: Turinblueice
Date: 2016/7/26
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import recycler_view

from appium.webdriver import WebElement

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from activities import activities
from selenium.common.exceptions import TimeoutException
from devices_manager import command_prompt

import time


class PersonalMainActivity(base_frame_view.BaseFrameView):

    """
    Summary:
        个人资料/in记主页

    Attributes:
        parent: 该活动页的父亲framework

    """

    name = '.diary.other.v260.DiaryOtherActivity'

    def __init__(self, parent):
        super(PersonalMainActivity, self).__init__(parent)

        self._scroll_view = frame_layout.FrameLayout(
            self.parent, id='com.jiuyan.infashion:id/drag_layout')

    # *****************************个人IN记页无,他人主页有,上层功能页********************************
    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/btn_diary_actionbar_back'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def live_button(self):
        """
            Summary:
                ta的直播按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_actionbar_live'
        return text_view.TextView(self.parent, id=id_)

    @property
    def follow_button(self):
        """
            Summary:
                关注/取消关注按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_actionbar_add'
        return text_view.TextView(self.parent, id=id_)

    @property
    def im_button(self):
        """
            Summary:
                聊天按钮
        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_nickname'
        return text_view.TextView(self.parent, id=id_)

    # ****************************封面信息**************************************
    @property
    def cover(self):
        """
            Summary:
                in记封面
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_holder'
        return frame_layout.FrameLayout(self.parent, id=id_)

    @property
    def user_nickname(self):
        """
            Summary:
                用户名称
        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_nickname'# 'com.jiuyan.infashion:id/login_tv_title'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def menu(self):
        """
            Summary:
                更多菜单
        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_menu'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def fans(self):
        """
            Summary:
                粉丝显示
        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_fans'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def fans_number(self):
        """
            Summary:
                粉丝个数
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/diary_user_header_fans_tv'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def photo_tab(self):
        """
            Summary:
                照片tab
        """
        id_ = 'com.jiuyan.infashion:id/layout_timeline'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def story_tab(self):
        """
            Summary:
                故事tab
        """
        id_ = 'com.jiuyan.infashion:id/layout_story'
        return linear_layout.LinearLayout(self.parent, id=id_)

    # *************************** 点击关注后可能出现的推荐感兴趣的人属性********************

    @property
    def friends_recommend_list(self):
        """
            Summary:
                推荐好友列表
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches("com.jiuyan.infashion:id/ll_diary_rec_friends_\d+")'
        return FriendRecommendItemList(self.parent, uiautomator=uiautomator_).item_list

    @property
    def friends_recommend_pull(self):
        """
            Summary:
                好友推荐收起按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_diary_rec_friends_pull_btn'
        return image_view.ImageView(self.parent, id=id_)

    # ******************************封面以下图片流元素**********************************

    @property
    def switch_button(self):
        """
            Summary:
                图片展示方式切换按钮
        """
        id_ = 'com.jiuyan.infashion:id/timeline_fabtn_layout'
        return button.Button(self.parent, id=id_)

    @property
    def matrix_photo_album_list(self):
        """
            Summary:
                矩阵式照片排列列表
        """
        rec_view = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/timeline_recycler')
        return PhotoAlbumItemList(rec_view, type='android.widget.FrameLayout').item_list

    @property
    def timeline_photo_album_list(self):
        """
            Summary:
                时间线方式的照片列表

        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/timeline_recycler\"]/' \
                 'android.widget.LinearLayout/' \
                 'android.widget.LinearLayout[not(@resource-id=\"com.jiuyan.infashion:id/ll_diary_self_header_message\")]/..'
        return PhotoAlbumItemList(self.base_parent, xpath=xpath_).timeline_item_list

    # *****************************取消关注的底部弹出元素********************************

    @property
    def unfollow_bottom_button(self):
        """
        Summary:
            取消关注按钮
        """
        id_ = 'com.jiuyan.infashion:id/cancel_watch'
        return text_view.TextView(self.parent, id=id_)

    @property
    def cancel_unfollow_bottom_button(self):
        """
        Summary:
            取消遮罩按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_cancel'
        return text_view.TextView(self.parent, id=id_)

    # *****************************更换封面********************************

    @property
    def change_cover_button(self):
        """
        Summary:
            更换封面按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_change_cover_from_gallery'
        return text_view.TextView(self.parent, id=id_)

    @property
    def cancel_change_cover_button(self):
        """
        Summary:
            取消更换封面按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_change_cover_from_gallery'
        return text_view.TextView(self.parent, id=id_)

    # **********************点击关注后出现的对话框*****************************

    @property
    def follow_dialogue(self):
        """
            Summary:
                关注对话框
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_content_bg'
        return FollowDialogue(self.parent, id=id_)

    # ***********************操作方法*********************************

    def tap_back_button(self):
        """
            Summary:
                点击后退按钮
        """
        log.logger.info("开始点击后退按钮")
        self.back_button.tap()
        log.logger.info("结束后退按钮点击")
        time.sleep(3)

    def tap_follow_button(self):
        """
            Summary:
                点击关注按钮
        """
        log.logger.info("开始点击关注按钮")
        self.follow_button.tap()
        log.logger.info("结束关注按钮点击")
        if self.wait_for_element_present(self.parent, timeout=3, id='com.jiuyan.infashion:id/dialog_content_bg'):
            log.logger.info("成功吊起关注对话框")
            return True
        log.logger.error("对话框未吊起")
        return False

    def is_friends_recommend_exist(self):
        """
            Summary:
                好友推荐是否存在
        Returns:

        """
        if self.wait_for_element_present(self.base_parent, timeout=3,
                                         id='com.jiuyan.infashion:id/iv_diary_rec_friends_pull_btn'):
            return True
        return False

    def tap_friends_pull_button(self):
        """
            Summary:
                点击好友推荐的收起按钮
        """
        log.logger.info("开始点击收起按钮")
        self.friends_recommend_pull.tap()
        log.logger.info("结束更多收起点击")
        time.sleep(2)

    def tap_more_button(self):
        """
            Summary:
                点击更多按钮
        """
        log.logger.info("开始点击更多按钮")
        self.menu.tap()
        log.logger.info("结束更多按钮点击")
        if self.wait_activity(activities.ActivityNames.REMARK, 10):
            log.logger.info("成功进入更改页面")
            return True
        log.logger.error("进入更改页面失败")
        return False

    def tap_unfollow_button(self):
        """
            Summary:
                点击取消关注按钮
        """
        log.logger.info("开始点击取消关注按钮")
        self.follow_button.tap()
        log.logger.info("结束取消关注按钮点击")
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/cancel_watch'):
            return True
        log.logger.error("弹出底部遮罩框失败")
        return False

    def tap_confirm_unfollow_button(self):
        """
            Summary:
                点击确认取消关注按钮
        """
        log.logger.info("开始点击确认取消关注按钮")
        self.unfollow_bottom_button.tap()
        log.logger.info("结束确认取消关注按钮点击")
        time.sleep(3)

    def tap_fans_button(self):
        """
            Summary:
                点击粉丝按钮
        Returns:

        """
        log.logger.info("开始点击粉丝按钮")
        self.fans.tap()
        if self.wait_activity(activities.ActivityNames.FOLLOWED_FANS_LIST, 10):
            log.logger.info("已经进入fans列表")
            return True
        log.logger.error("进入fans列表失败")
        return False

    def tap_switch_button(self):
        """
            Summary:
                看图模式切换按钮
        Returns:

        """
        log.logger.info("点击切换按钮")
        self.switch_button.tap()
        log.logger.info("看图模式切换完毕")
        time.sleep(5)

    def tap_diary_cover(self):
        """
            Summary:
                点击in记封面
        Returns:

        """
        log.logger.info("点击in记头部的封面")
        self.cover.tap()
        if self.wait_for_element_present_under_alert(self.base_parent,
                                                     id='com.jiuyan.infashion:id/tv_diary_change_cover_from_gallery'):
            log.logger.info("成功吊起底部遮罩")
            return True
        log.logger.error("吊起底部遮罩失败")
        return False

    def tap_change_cover_button(self):
        """
            Summary:
                点击更换封面按钮
        Returns:

        """
        log.logger.info('点击更换封面按钮')
        self.change_cover_button.tap()
        log.logger.info("完成更换封面按钮的点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_PICKER, 10):
            log.logger.info("成功进入图片选择页面")
            return True
        log.logger.error("进入图片选择页面失败")
        return False

    def swipe_up_entire_scroll_view(self):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + size['width']*0.7
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")


class PhotoAlbumItem(base_frame_view.BaseFrameView):
    """
        Summary:
            照片列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(PhotoAlbumItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def photo_count(self):

        id_ = 'com.jiuyan.infashion:id/tv_number_multi_photo'
        return text_view.TextView(self._layout_view, id=id_).text

    #  **********************操作方法************************
    def tap(self, tap_count=1):
        """
            Summary:
                点击图片集
        """
        log.logger.info("开始点击该图片集")

        for _ in range(tap_count):
            self._layout_view.click()  # 尚未知道点击两下图片, 应用才响应的原因

        if self.wait_activity(activities.ActivityNames.PHOTO_ALBUM_CORE, 10):
            log.logger.info("成功进入图片集详情页")
            return True
        log.logger.error("进入图片集详情页失败")
        return False


class TimelinePhotoAlbumItem(base_frame_view.BaseFrameView):
    """
        Summary:
            矩阵式照片列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(TimelinePhotoAlbumItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def date(self):

        id_ = 'com.jiuyan.infashion:id/tv_date_day'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def month(self):

        id_ = 'com.jiuyan.infashion:id/tv_date_month'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def photo_album_frame(self):
        """
            Summary:
                图片集框
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/inlcl_diary_timeline'
        return view.View(self._layout_view, id=id_)

    @property
    def photo_list(self):
        """
            Summary:
                照片列表,一般为三张
        Returns:

        """

        id_ = 'com.jiuyan.infashion:id/iv'
        return image_view.ImageViewList(self._layout_view, id=id_).image_list

    @property
    def photo_desc(self):
        """
            Summary:
                照片描述
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_timeline_desc'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def view_count(self):
        """
            Summary:
                浏览量
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_count_view'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def like_count(self):
        """
            Summary:
                点赞数
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_count_zan'
        return text_view.TextView(self._layout_view, id=id_).text

    #  **********************操作方法************************
    def tap(self):
        """
            Summary:
                点击图片集
        """
        log.logger.info("开始点击该图片集")
        self.photo_album_frame.tap()
        if self.wait_activity(activities.ActivityNames.PHOTO_ALBUM_CORE, 10):
            log.logger.info("成功进入图片集详情页")
            return True
        log.logger.error("进入图片集详情页失败")
        return False


class PhotoAlbumItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PhotoAlbumItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [PhotoAlbumItem(item.parent, item) for item in self.__list]
        return None

    @property
    def timeline_item_list(self):
        if self.__list:
            return [TimelinePhotoAlbumItem(item.parent, item) for item in self.__list]
        return None

# **********************点击关注后出现的对话框*****************************


class FollowDialogue(base_frame_view.BaseFrameView):
    """
        Summary:
            关注对话框
    """
    def __init__(self, parent, **kwargs):
        super(FollowDialogue, self).__init__(parent)
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
    def interest_group(self):
        """
            Summary:
                订阅分组
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_chose_friend_type_ll_interest'
        return linear_layout.LinearLayout(self._dialogue, id=id_)

    @property
    def remark_edit_box(self):
        """
            Summary:
                名称编辑框
        Returns:

        """

        id_ = 'com.jiuyan.infashion:id/dialog_et_nickname'
        return edit_text.EditText(self._dialogue, id=id_)

    @property
    def ok_button(self):
        """
            Summary:
                完成按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/dialog_tv_ok'
        return text_view.TextView(self._dialogue, id=id_)

    # ********************操作方法*******************

    def select_group(self, group_name='friend'):
        """

        Args:
            group_name: 两个值friend表示勾选朋友,interest表示勾选订阅

        Returns:

        """
        words = {'friend': '朋友', 'interest': '订阅'}

        if group_name in ('friend', 'interest'):
            log.logger.info("开始点击\"{}\"分组".format(words[group_name]))
            getattr(self, group_name+'_group', None).tap()
            log.logger.info("点击完毕")
            log.logger.info("检查是否已选中\"{}\"分组".format(words[group_name]))
            try:
                WebDriverWait(self.base_parent, 3).until(
                    (MobileBy.ID, 'com.jiuyan.infashion:id/dialog_chose_friend_type_tv_{}'.format(group_name))
                )
                log.logger.info("已选中\"{}\"分组".format(words[group_name]))
                return True
            except:
                log.logger.error("选择\"{}\"分组失败".format(words[group_name]))
                return False
        else:
            log.logger.error("group_name值错误,只能选择friend或者interest")
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

# ******************推荐好友列表******************


class FriendRecommendItem(base_frame_view.BaseFrameView):
    """
        Summary:
            照片列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(FriendRecommendItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def avatar(self):
        """
            Summary:
                头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/civ_diary_rec_friends_avatar'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def user_name(self):
        """
            Summary:
                名称
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_rec_friends_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def follow_button(self):
        """
            Summary:
                关注按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_diary_rec_friends_follow'
        return text_view.TextView(self._layout_view, id=id_)

    #  **********************操作方法************************


class FriendRecommendItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(FriendRecommendItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [FriendRecommendItem(item.parent, item) for item in self.__list]
        return None


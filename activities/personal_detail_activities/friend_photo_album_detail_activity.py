#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:好友图片详情页

Authors: Turinblueice
Date: 2016/9/10
"""

from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import edit_text

from appium.webdriver import WebElement
from activities import activities
import time


class FriendPhotoDetailActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            好友图片详情页面
            发现-话题-点击某话题-点击具体话题-点击话题图片页

        Attributes:

    """
    name = '.friend.activity.FriendPhotoDetailActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(FriendPhotoDetailActivity, self).__init__(parent)
        #  等待页面网络请求进行初始化
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/friend_title_bar'):
            self._scroll_view = frame_layout.FrameLayout(self.parent,
                                                         id='com.jiuyan.infashion:id/lv_friend_photo_detail_comment_list')
        else:
            raise

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_friend_back'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def user_avatar(self):
        """
            Summary:
                用户头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def photo_list(self):
        """
            Summary:
                照片集列表
        :return:
        """
        xpath_ = '//android.view.View[@resource-id=\"com.jiuyan.infashion:id/friend_photo_detail_nine_cell\"]/' \
                 'android.widget.FrameLayout'
        return frame_layout.FrameLayoutList(self.base_parent, xpath=xpath_).frame_list

    @property
    def tag_list(self):
        """
            Summary:
                标签列表
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_right'
        return text_view.TextViewList(self.parent, id=id_).text_view_list

    @property
    def zan_button(self):
        """
            Summary:
                点赞按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_friend_photo_detail_like'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def zan_count(self):
        """
            Summary:
                点赞数
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/civ_friend_photo_detail_like_num'
        try:
            zancount = text_view.TextView(self.parent, id=id_).text
            return zancount
        except:
            return '0'

    @property
    def more_menu(self):
        """
            Summary:
                更多按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_friend_photo_detail_more'
        return image_view.ImageView(self.parent, id=id_)

    # ************************评论内容***********************************
    @property
    def latest_comment_value(self):
        """
            Summary:
                最新评论
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_friend_item_comment_content'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def latest_comment_user(self):
        """
            Summary:
                最新评论人
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_friend_item_comment_user_name'
        return text_view.TextView(self.parent, id=id_).text

    # **************************底部发表控件*******************************

    @property
    def edit_box(self):
        """
            Summary:
                文本输入框
        """
        id_ = 'com.jiuyan.infashion:id/et_content'
        return edit_text.EditText(self.parent, id=id_)

    @property
    def send_button(self):
        """
            Summary:
                发送按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_send'
        return text_view.TextView(self.parent, id=id_)

    # **************************操作方法*****************************

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

    def tap_photo(self, index=0):
        """
            Summary:
                点击图片
            Args:
                index: 图片序号
        Returns:

        """
        log.logger.info("开始点击第{}张图片".format(index+1))
        self.photo_list[index].tap()
        log.logger.info("完成图片点击")
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_VIEW, 10):
            log.logger.info("成功进入图片页")
            return True
        log.logger.error("进入图片页失败")
        return False

    def tap_tag(self, index=0):
        """
            Summary:
                点击标签
        Args:
            index:标签序号

        Returns:

        """
        log.logger.info("点击第{}个标签".format(index + 1))
        self.tag_list[index].tap()
        log.logger.info("标签点击完毕")
        if self.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功进入话题标签详情页")
            return True
        log.logger.error("进入话题标签详情页失败")
        return False

    def tap_zan(self):
        """
            Summary:
                点赞
        Returns:

        """
        curr_zan_count = int(self.zan_count)
        log.logger.info("开始点赞")
        self.zan_button.tap()
        log.logger.info("点赞完毕")
        if not self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/civ_friend_photo_detail_like_num'):
            self.swipe_up_entire_scroll_view()
        now_count = int(self.zan_count)
        return now_count == curr_zan_count + 1

    def remove_zan(self):
        """
            Summary:
                取消点赞
        Returns:

        """
        curr_zan_count = int(self.zan_count)
        log.logger.info("取消点赞")
        self.zan_button.tap()
        log.logger.info("取消点赞完毕")
        time.sleep(2)
        now_count = int(self.zan_count)
        return now_count == curr_zan_count - 1

    def tap_back_button(self):
        """
            Summary:
                点击返回按钮
        """
        log.logger.info("开始点击返回按钮")
        self.back_button.tap()
        if self.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功返回到话题页")
            return True
        log.logger.error("返回话题页失败")
        return False

    def input_comment(self, value):
        """
            Summary:
                输入文字
        """
        value = value.encode('utf8') if isinstance(value, unicode) else value
        log.logger.info("开始输入文字:{}".format(value))
        self.edit_box.clear_text_field()
        self.edit_box.set_text(value)
        time.sleep(2)
        log.logger.info("完成输入")

    def tap_send_button(self):
        """
            Summary:
                点击发送按钮
        """
        log.logger.info("开始点击发送按钮")
        self.send_button.tap()
        time.sleep(2)
        log.logger.info("完成发送")
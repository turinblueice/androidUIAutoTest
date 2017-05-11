#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:

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

from appium.webdriver import WebElement
from appium.webdriver.common import touch_action
from selenium.webdriver.common.touch_actions import TouchActions
from activities import activities
import time


class TopicDetailActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            话题详情页

        Attributes:

    """
    name = '.module.tag.activity.TagActivityV253'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(TopicDetailActivity, self).__init__(parent)
        #  等待页面网络请求进行初始化
        self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/toolbar')
        self._scroll_view = frame_layout.FrameLayout(self.parent, id='com.jiuyan.infashion:id/drag_layout')

    @property
    def title(self):
        """
            Summary:
                活动页标题
        """
        id_ = 'com.jiuyan.infashion:id/tv_title'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_left'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def more_menu(self):
        """
            Summary:
                 更多按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_right'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def subscription_button(self):
        """
            Summary:
                订阅按钮
        """
        id_ = 'com.jiuyan.infashion:id/subscribe'
        return frame_layout.FrameLayout(self.parent, id=id_)

    @property
    def subscription_text(self):
        """
            Summary:
                订阅文字
        """
        id_ = 'com.jiuyan.infashion:id/tv_subscribe'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def heat_button(self):
        """
            Summary:
                加热按钮
        """
        id_ = 'com.jiuyan.infashion:id/unsub_up_hot'
        return text_view.TextView(self.parent, id=id_)

    @property
    def hotest_tab(self):
        """
            Summary:
                最热tab
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/layout_title_hotest'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def newest_tab(self):
        """
            Summary:
                最新tab
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/layout_title_newest'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def post_button(self):
        """
            Summary:
                发帖按钮
        """
        id_ = 'com.jiuyan.infashion:id/layout_post'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def newest_photo_album_list(self):
        """
            Summary:
                最新tab下的照片集列表
        :return:
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/recycler"]/' \
                 'android.widget.LinearLayout'
        return NewestPhotoAlbumList(self.base_parent, xpath=xpath_).item_list

    @property
    def hotest_container_list(self):
        """
            Summary:
                最热内容列表
        """
        id_ = 'com.jiuyan.infashion:id/ll_hottest_container'
        return HotestContainerList(self.parent, id=id_).item_list

    # **************************订阅成功后的属性*******************************
    @property
    def subscribe_attention(self):
        """
            Summary:
                订阅成功提示
        """
        id_ = 'com.jiuyan.infashion:id/tag_subscripe_ll'
        return linear_layout.LinearLayout(self.parent, id=id_)

    # ******************************点击菜单后遮罩按钮****************************************

    @property
    def share_pop_button(self):
        """
            Summary:
                遮罩分享按钮
        """
        return text_view.TextView(self.parent, uiautomator='new UiSelector().text("分享")')

    @property
    def undo_subscribe_button(self):
        """
            Sumary:
                取消订阅按钮
        """
        return text_view.TextView(self.parent, uiautomator='new UiSelector().text("取消订阅")')

    @property
    def cancel_pop_button(self):
        """
            Summary:
                取消按钮
        """
        return text_view.TextView(self.parent, id='com.jiuyan.infashion:id/tv_bottom_menu_cancel')

    # **************************操作方法*****************************
    def wait_for_hotest_container(self):
        """
            Summary:
                等待网络请求获得最热门内容
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/rv_tag_hottest'
        rec_ = recycler_view.RecyclerView(self.parent, id=id_)
        if self.wait_for_element_present(rec_, timeout=15, id='com.jiuyan.infashion:id/ll_hottest_container'):
            log.logger.info("最热内容已记载")
            return True
        log.logger.error("最热内容加载失败")
        return False

    def wait_for_newest_photo_album(self):
        """
            Summary:
                等待网络请求获得最新的照片集合
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/recycler'
        rec_ = recycler_view.RecyclerView(self.parent, id=id_)
        if self.wait_for_element_present(rec_, timeout=10, type='android.widget.LinearLayout'):
            log.logger.info("最新图片集合已加载")
            return True
        log.logger.error("最新图片加载失败")
        return False

    def tap_clear_subscribe_attention(self):
        """
            Summary:
                点击取消订阅提示
        """
        log.logger.info("开始点击取消订阅提示")
        self.tap_window_top()
        time.sleep(2)
        log.logger.info("完成取消")

    def tap_subscription_button(self):
        """
            Summary:
                点击订阅按钮
        """
        log.logger.info("开始点击订阅按钮")
        self.subscription_button.tap()
        time.sleep(2)
        log.logger.info("完成点击")

    def is_subscribe_successful(self):
        """
            Summary:
                订阅是否成功
        """
        try:
            status = self.subscription_button.is_displayed()
            return status
        except:
            return False

    def tap_more_menu(self):
        """
            Summary:
                点击更多按钮
        """
        log.logger.info("开始点击更多按钮")
        self.more_menu.tap()
        time.sleep(2)
        log.logger.info("点击更多按钮完毕")
        try:
            status = self.cancel_pop_button.is_displayed()
            return status
        except:
            return False

    def tap_undo_subscription_button(self):
        """
            Summary:
                点击取消订阅按钮
        """
        log.logger.info("开始点击取消订阅按钮")
        self.undo_subscribe_button.tap()
        time.sleep(2)
        log.logger.info("完成点击")

    def tap_newest_tab(self):
        """
            Summary:
                点击最新tab
        """
        log.logger.info("开始点击最新按钮")
        self.newest_tab.tap()
        time.sleep(2)
        log.logger.info("完成点击")

    def tap_hotest_tab(self):
        """
            Summary:
                点击最热tab
        """
        log.logger.info("开始点击最热按钮")
        self.hotest_tab.tap()
        time.sleep(2)
        log.logger.info("完成点击")

    def swipe_down_entire_scroll_view(self):
        """
            Summary:
                重写向下滑动方法，因为向下滑动时，顶部的tab影响初始滑动的坐标，所以需要加上tab高度进行滑动
                向下滑动整个scroll view的高度
        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + size['width']/2
        end_y = location['y'] + size['height'] - 1

        step_height = self.newest_tab.size['height']
        start_y = location['y'] + step_height + 2

        log.logger.info("开始向下滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向下滑动结束")

    def swipe_up_half_scroll_view(self):
        """
            Summary:
                向上滑动半个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = location['x'] + size['width']/2
        start_y = location['y'] + size['height']/2
        end_y = location['y']

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")


class HotestContainer(base_frame_view.BaseFrameView):
    """
        Summary:
            最热内容列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(HotestContainer, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def up_name(self):
        """
            Summary:
                楼主姓名
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def viewer_count(self):
        """
            Summary:
                观看人数
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_view'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def date(self):
        """
            Summary:
                日期
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_date'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def description(self):
        """
            Summary:
                文本内容描述
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_desc'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def like_button(self):
        """
            Summary:
                点赞按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_like'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def like_count(self):
        """
            Summary:
                点赞数
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_like'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def liker_avatar_list(self):
        """
            Summary:
                点赞人数头像列表
        """
        layout = linear_layout.LinearLayout(self._layout_view, id_='com.jiuyan.infashion:id/ll_tag_hottest_liker')
        liker_list = image_view.ImageViewList(layout, type='android.widget.ImageView').image_list[:-1]
        return liker_list

    @property
    def latest_comment(self):
        """
            Summary:
                最新的一条评论
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_comment_1'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def submit_button(self):
        """
            Summary:
                发表框，“我也说一句”
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag_hottest_comment_submit'
        return text_view.TextView(self._layout_view, id=id_)

    # ********************操作方法*************************

    def do_like(self):
        """
            Summary:
                点赞

        """
        log.logger.info("开始点赞")
        self.like_button.tap()
        time.sleep(2)
        log.logger.info("点赞完毕")

    def undo_like(self):
        """
            Summary:
                取消点赞
        """
        log.logger.info("开始取消点赞")
        self.like_button.tap()
        time.sleep(2)
        log.logger.info("取消完毕")

    def tap_to_submit_comment(self):
        """
            Summary:
                点击发表评论
        """
        log.logger.info("开始点击发表评论")
        self.submit_button.tap()
        log.logger.info("已经完成发表评论点击")
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_DETAIL, 10):
            log.logger.info("成功进入图片详情页")
            return True
        log.logger.error("进入图片详情页失败")
        return False


class HotestContainerList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(HotestContainerList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [HotestContainer(item.parent, item) for item in self.__list]
        return None


class NewestPhotoAlbum(base_frame_view.BaseFrameView):
    """
        Summary:
            照片列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(NewestPhotoAlbum, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def like_count(self):
        """
            Summary:
                点赞数
        """
        id_ = 'com.jiuyan.infashion:id/tv_like'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def like_icon(self):
        """
            Summary:
                点赞图标
        """
        id_ = 'com.jiuyan.infashion:id/iv_like'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def title(self):
        """
            Summary:
                图片集合标题
        """
        id_ = 'com.jiuyan.infashion:id/tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def photo_count(self):
        """
            Summary：
                照片数量
        """
        id_ = 'com.jiuyan.infashion:id/iv_number'
        return text_view.TextView(self.parent, id=id_).text

    # ********************操作方法*************************
    def tap_like_button(self, like=True):
        """
            Summary:
                 点赞
        Returns:

        """
        old_count = self.like_count if not self.like_count == 'like' else '0'
        log.logger.info("开始点击点赞按钮")
        self.like_icon.tap()
        log.logger.info("点赞完毕")
        curr_count = self.like_count
        if like:
            if old_count in ('999', '999+'):
                if curr_count == '999+':
                    log.logger.info("点赞前点赞数{},当前点赞数{}".format(old_count, curr_count))
                    return True
                return False
            else:
                log.logger.info("点赞前点赞数{},当前点赞数{}".format(old_count, curr_count))
                return int(old_count) + 1 == int(curr_count)
        else:
            if old_count == '999+':
                if curr_count in ('999', '999+'):
                    log.logger.info("点赞前点赞数{},当前点赞数{}".format(old_count, curr_count))
                    return True
                return False
            else:
                log.logger.info("点赞前点赞数{},当前点赞数{}".format(old_count, curr_count))
                return int(old_count) - 1 == int(curr_count)

    def double_tap(self):
        """。
            Summary:
                双击点赞/取消点赞
        """
        log.logger.info("开始双击")
        # x = self._layout_view.size['width']/2
        # y = self._layout_view.size['height']/2
        # opts = {
        #     'element': self._layout_view.id,
        #     'x': x,
        #     'y': y,
        #     'tapCount': 2.0,
        # }
        # self.base_parent.execute_script('mobile:tap', opts)

        tc = TouchActions(self.base_parent)
        tc.double_tap(self._layout_view)
        tc.perform()

        log.logger.info("双击完毕")
        time.sleep(2)

    def tap(self):
        """
            Summary:
                点击进入图片详情页
        """
        log.logger.info("开始点击图片")
        self._layout_view.click()
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_DETAIL, 10):
            log.logger.info("成功进入图片详情页")
            return True
        log.logger.error("进入图片详情页失败")
        return False


class NewestPhotoAlbumList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(NewestPhotoAlbumList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [NewestPhotoAlbum(item.parent, item) for item in self.__list]
        return None

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

from gui_widgets.basic_widgets import view_pager
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import recycler_view

from appium.webdriver import WebElement
from appium.webdriver.common import touch_action
from selenium.webdriver.common.touch_actions import TouchActions
from activities import activities
import time


class EssenceRecommendActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            精选推荐页

        Attributes:

    """
    name = '.module.square.activity.EssenceRecActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(EssenceRecommendActivity, self).__init__(parent)
        self._scroll_view = view_pager.ViewPager(self.parent,
                                                 id='com.jiuyan.infashion:id/square_viewpager_essence')

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/iv_left'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def tab_list(self):
        """
            Summary:
                tab列表
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_title'
        return text_view.TextViewList(self.parent, id=id_).text_view_list

    @property
    def photo_list(self):
        """
            Summary:
                最热内容列表
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/essence_recyclerview"]' \
                 '/android.widget.LinearLayout'
        return PhotoAlbumList(self.base_parent, xpath=xpath_).item_list

    # **************************操作方法*****************************

    def wait_for_newest_photo_album(self, timeout=10):
        """
            Summary:
                等待网络请求获得最新的照片集合
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/rl_photo'
        if self.wait_for_element_present(self._scroll_view, timeout=timeout, id=id_):
            log.logger.info("最新图片集合已加载")
            return True
        log.logger.error("最新图片加载失败")
        return False


class PhotoAlbum(base_frame_view.BaseFrameView):
    """
        Summary:
            照片列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(PhotoAlbum, self).__init__(parent)
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

        try:
            count = text_view.TextView(self.parent, id=id_).text
            return count
        except:
            return '0'

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
                return int(old_count)+1 == int(curr_count)
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
                点击进入图片/故事集详情页
        """
        log.logger.info("开始点击图片")
        self._layout_view.click()
        if self.wait_one_of_activities((activities.ActivityNames.FRIEND_PHOTO_DETAIL, activities.ActivityNames.STORY_DETAIL), timeout=10):
            log.logger.info("成功进入图片/故事集详情页")
            return True
        log.logger.error("进入图片/故事集详情页失败")
        return False


class PhotoAlbumList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PhotoAlbumList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [PhotoAlbum(item.parent, item) for item in self.__list]
        return None

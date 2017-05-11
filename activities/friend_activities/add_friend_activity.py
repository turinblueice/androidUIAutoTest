#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 添加好友页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import list_view
from gui_widgets.basic_widgets import grid_view

from appium.webdriver import WebElement
from activities import activities
import time


class AddFriendActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            添加好友页面

        Attributes:

    """
    name = '.lib.component.cropper.CropperActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(AddFriendActivity, self).__init__(parent)

    @property
    def back_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = "com.jiuyan.infashion:id/iv_usercenter_setting_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def add_friend_category_bar(self):
        """
            Summary:
                增加好友的种类滑动栏
        """
        id_ = "com.jiuyan.infashion:id/rv_uc_add_friends_category"
        return recycler_view.RecyclerView(self.parent, id=id_)

    #  ***********************明星达人tab下的元素******************************

    @property
    def star_talent_item(self):
        """
            Summary:
                明星达人添加按钮
        """
        return text_view.TextView(self.parent, uiautomator='new UiSelector().textContains(\"明星达人\")')

    @property
    def start_talent_follow_friends_list(self):
        """
            Summary:
                明星达人推荐列表
        """
        xpath_ = '//android.widget.ListView[@resource-id=\"com.jiuyan.infashion:id/usercenter_follow_friends_list\"]/' \
                 'android.widget.LinearLayout'
        return StarTalentItemList(self.base_parent, xpath=xpath_).item_list

    # ************************操作***************************

    def tap_back_button(self):
        """
            Summary:
                点击返回按钮
        """
        log.logger.info("开始点击返回按钮")
        self.back_button.tap()
        log.logger.info("完成返回按钮点击")
        if self.wait_activity(activities.ActivityNames.IN_MAIN, 10):
            log.logger.info("成功回到主页")
            return True
        log.logger.error("回到主页失败")
        return False

    def tap_start_talent_item(self):
        """
            Summary:
                点击明星达人按钮
        """
        log.logger.info("开始点击明星达人按钮")
        self.star_talent_item.tap()
        log.logger.info("完成明星达人按钮的点击")
        view_ = list_view.ListView(self.parent, id='com.jiuyan.infashion:id/usercenter_follow_friends_list')
        if self.wait_for_element_present(view_, type='android.widget.LinearLayout'):
            log.logger.info("达人已经加载")
            return True
        log.logger.error("达人未加载")
        return False

    def swipe_left_friend_category(self):
        """
            Summary:
                向左边滑动好友种类栏
        """
        location = self.add_friend_category_bar.location
        size = self.add_friend_category_bar.size
        y = location['y'] + size['height']/2
        start_x = location['x'] + size['width'] - 1
        end_x = location['x'] + 1

        log.logger.info("开始向左边滑动整个好友种类栏")
        self.swipe_left(start_x, end_x, y)
        log.logger.info("向左边滑动结束")
        time.sleep(3)


class StarTalentItem(base_frame_view.BaseFrameView):
    """
        Summary:
            明星达人item类
    """
    def __init__(self, parent, item=None, **kwargs):
        super(StarTalentItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def user_name(self):
        """
            Summary:
                用户名称
        """
        id_ = 'com.jiuyan.infashion:id/tv_follow_friends_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def follow_button(self):
        """
            Summary:
                关注按钮
        """
        id_ = 'com.jiuyan.infashion:id/follow_friends_follow_btn'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def photo_album_list(self):
        """
            Summary:
                照片列表
        """
        grid_ = grid_view.GridView(self._layout_view, id='com.jiuyan.infashion:id/gv_follow_friends_photo')
        return PhotoAlbumItemList(grid_, type='android.widget.RelativeLayout').item_list

    #  ******************************操作方法********************************

    def tap_follow_button(self):
        """
            Summary:
                点击关注按钮
        """
        log.logger.info("开始点击关注按钮")
        self.follow_button.tap()
        log.logger.info("完成关注按钮点击")
        time.sleep(2)


class StarTalentItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(StarTalentItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [StarTalentItem(item.parent, item) for item in self.__list]
        return None


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

        id_ = 'com.jiuyan.infashion:id/tv_follow_friends_photo_num'
        return text_view.TextView(self._layout_view, id=id_).text


class PhotoAlbumItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PhotoAlbumItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [PhotoAlbumItem(item.parent, item) for item in self.__list]
        return None

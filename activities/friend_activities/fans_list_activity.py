#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: fans列表

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import view
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view

from appium.webdriver import WebElement
from activities import activities
import time


class FansListActivity(base_frame_view.BaseFrameView):

    """
        Summary:
             粉丝列表

        Attributes:

    """
    name = '.diary.follower.FollowedListActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(FansListActivity, self).__init__(parent)
        self._scroll_view = view.View(self.parent, id='com.jiuyan.infashion:id/diary_followed_refresh')

    @property
    def back_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = "com.jiuyan.infashion:id/diary_followed_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def fans_list(self):
        """
            Summary:
                明星达人推荐列表
        """
        xpath_ = '//android.widget.ListView[@resource-id=\"com.jiuyan.infashion:id/diary_followed_listview\"]/' \
                 'android.widget.LinearLayout'
        try:
            return FansList(self.base_parent, xpath=xpath_).item_list
        except:
            return None

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
            log.logger.info("成功回到个人in记页")
            return True
        log.logger.error("回到个人in记页失败")
        return False


class FansItem(base_frame_view.BaseFrameView):
    """
        Summary:
            明星达人item类
    """
    def __init__(self, parent, item=None, **kwargs):
        super(FansItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def user_name(self):
        """
            Summary:
                用户名称
        """
        id_ = 'com.jiuyan.infashion:id/tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def desc(self):
        """
            Summary:
                关注按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def avatar(self):
        """
            Summary:
                照片列表
        """
        id_ = 'com.jiuyan.infashion:id/civ_avatar'
        return image_view.ImageView(self._layout_view, id=id_)

    #  ******************************操作方法********************************

    def tap(self):
        """
            Summary:
                点击进入个人主页
        """
        user_name = self.user_name
        log.logger.info("开始点击该粉丝:{}".format(user_name))
        self._layout_view.click()
        log.logger.info("完成粉丝点击")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入用户\"{}\"的in主页".format(user_name))
            return True
        log.logger.error("进入用户\"{}\"的in主页失败".format(user_name))
        return False


class FansList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(FansList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [FansItem(item.parent, item) for item in self.__list]
        return None

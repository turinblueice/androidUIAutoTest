#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:话题广场页

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


class TopicSquareActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            话题广场页面

        Attributes:

    """
    name = '.module.square.men.activity.SquareMenTopicActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(TopicSquareActivity, self).__init__(parent)
        self._scroll_view = frame_layout.FrameLayout(self.parent, id='com.jiuyan.infashion:id/base_fragment_id')

    @property
    def my_tab(self):
        """
            Summary:
                我的tab
        """
        id_ = 'com.jiuyan.infashion:id/square_men_tag_all_tv_me'
        return text_view.TextView(self.parent, id=id_)

    @property
    def recommend_tab(self):
        """
            Summary:
                推荐tab
        """
        id_ = 'com.jiuyan.infashion:id/square_men_tag_all_tv_recommend'
        return text_view.TextView(self.parent, id=id_)

    @property
    def category_tab(self):
        """
            Summary:
                分类tab
        """
        id_ = 'com.jiuyan.infashion:id/square_men_tag_all_tv_all'
        return text_view.TextView(self.parent, id=id_)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/square_men_tag_all_tv_back'
        return text_view.TextView(self.parent, id=id_)

    @property
    def create_button(self):
        """
            Summary:
                 创建按钮
        """
        id_ = 'com.jiuyan.infashion:id/square_men_tag_all_tv_create'
        return text_view.TextView(self.parent, id=id_)

    # ***********************分类话题tab下的元素******************************

    @property
    def category_list(self):
        """
            Summary:
                分类tab下的类目列表
        Returns:

        """
        xpath_ = '//android.widget.ListView[@resource-id=\"com.jiuyan.infashion:id/square_rv_menu\"]/' \
                 'android.widget.LinearLayout'
        return linear_layout.LinearLayoutList(self.base_parent, xpath=xpath_).layout_list

    @property
    def topic_list(self):
        """
            Summary:
                分类tab下的右侧话题列表
        Returns:

        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/square_rv_tag\"]/' \
                 'android.widget.LinearLayout'
        return TopicItemList(self.parent, xpath=xpath_).item_list

    # **********************我的话题tab的话题列表*************************

    @property
    def my_topic_list(self):
        """
            Summary:
                我的tab下的右侧话题列表
        Returns:

        """
        xpath_ = '//android.widget.ExpandableListView[@resource-id=\"com.jiuyan.infashion:id/usercenter_topic_list\"]/' \
                 'android.widget.RelativeLayout'
        return MyTopicItemList(self.parent, xpath=xpath_).item_list

    # **************************操作方法*****************************

    def tap_my_tab(self):
        """
            Summary:
                点击我的tab
        Returns:

        """
        log.logger.info("开始点击\"我的\"tab")
        self.my_tab.tap()
        log.logger.info("点击完毕")
        time.sleep(3)

    def tap_recommend_tab(self):
        """
            Summary:
                点击推荐tab
        Returns:

        """
        log.logger.info("开始点击\"推荐\"tab")
        self.recommend_tab.tap()
        log.logger.info("点击完毕")
        time.sleep(3)

    def tap_category_tab(self):
        """
            Summary:
                点击推荐tab
        Returns:

        """
        log.logger.info("开始点击\"分类\"tab")
        self.category_tab.tap()
        log.logger.info("点击完毕")
        time.sleep(3)


class TopicItem(base_frame_view.BaseFrameView):
    """
        Summary:
            分类tab下的话题列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(TopicItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def topic_name(self):
        """
            Summary:
                话题名
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_title'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def view_count(self):
        """
            Summary:
                观看数
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_watch_count'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def image_count(self):
        """
            Summary:
                图片数
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_image_count'
        return text_view.TextView(self._layout_view, id=id_).text

    # ********************操作方法*************************

    def tap(self):
        """
            Summary:
                点击话题
        """
        topic = self.topic_name
        log.logger.info("开始点击\"{}\"话题".format(topic))
        self._layout_view.click()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功进入话题页")
            return True
        log.logger.error("进入话题页失败")
        return False


class TopicItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(TopicItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [TopicItem(item.parent, item) for item in self.__list]
        return None


class MyTopicItem(base_frame_view.BaseFrameView):
    """
        Summary:
            我的tab下的话题列表
    """
    def __init__(self, parent, item=None, **kwargs):
        super(MyTopicItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def topic_name(self):
        """
            Summary:
                话题名
        """
        id_ = 'com.jiuyan.infashion:id/uc_tv_topic_title'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def view_count(self):
        """
            Summary:
                观看数
        """
        id_ = 'com.jiuyan.infashion:id/uc_tv_hot_topic_read_count'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def image_count(self):
        """
            Summary:
                图片数
        """
        id_ = 'com.jiuyan.infashion:id/uc_tv_hot_topic_pic_count'
        return text_view.TextView(self._layout_view, id=id_).text

    # ********************操作方法*************************

    def tap(self):
        """
            Summary:
                点击话题
        """
        topic_name = self.topic_name
        log.logger.info("开始点击\"{}\"话题".format(topic_name))
        self._layout_view.click()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功进入话题页")
            return True
        log.logger.error("进入话题页失败")
        return False


class MyTopicItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(MyTopicItemList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [MyTopicItem(item.parent, item) for item in self.__list]
        return None

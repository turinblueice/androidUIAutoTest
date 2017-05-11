#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-我的贴纸

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import linear_layout

from gui_widgets.custom_widgets import search_bar
from activities import activities

from appium.webdriver import WebElement
import time


class UserPasterActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            用户中心-我的贴纸

        Attributes:

    """
    name = '.module.paster.activity.PasterMallActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(UserPasterActivity, self).__init__(parent)
        self._scroll_view = None

    @property
    def scroll_view(self):
        return self._scroll_view

    @property
    def search_bar(self):
        """
            Summary:
                搜索栏
        """
        return search_bar.PasterSearchBar(self.parent)

    @property
    def tab_bar(self):
        """
            Summary:
                搜索栏下面的tab栏
        """

        return TabRecycler(self.parent)

    @property
    def back_button(self):

        id_ = 'com.jiuyan.infashion:id/actionbar_btn_back'
        return linear_layout.LinearLayout(self.parent, id=id_)

    # *******************操作方法**************************

    def tap_back_button(self, window=activities.ActivityNames.PUBLISH_CORE):

        log.logger.info("点击返回按钮")
        self.back_button.tap()
        log.logger.info('完成返回按钮点击')
        if self.wait_activity(window, 10):
            log.logger.info("回到指定的页面")
            return True
        log.logger.error("回到指定页面失败")
        return False


class TabRecycler(recycler_view.RecyclerView):

    def __init__(self, parent):
        super(TabRecycler, self).__init__(parent, type='android.support.v7.widget.RecyclerView')

    @property
    def tab_list(self):
        """
            Summary:
                搜索结果列表
        """
        xpath_ = '//android.widget.ListView[1]/android.widget.LinearLayout'
        return TabList(self.base_parent, xpath=xpath_).item_list

    @property
    def my_own_tab(self):
        """
            Summary:
                “我的”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="我的"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def recommend_tab(self):
        """
            Summary:
                “推荐”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="推荐"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def recommend_tab(self):
        """
            Summary:
                “推荐”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="推荐"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def decoration_tab(self):
        """
            Summary:
                “装饰”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="装饰"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def cartoon_tab(self):
        """
            Summary:
                “卡通”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="卡通"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def words_tab(self):
        """
            Summary:
                “文字”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="文字"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def theme_tab(self):
        """
            Summary:
                “主题”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="主题"]/../..'
        return TabItem(self.base_parent, xpath=xpath_)


class TabItem(base_frame_view.BaseFrameView):
    """
        Summary:
            顶部tab类
    """

    def __init__(self, parent, item=None, **kwargs):
        super(TabItem, self).__init__(parent)
        self.__item = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def title(self):
        """
            Summary:
                推荐item的内容
        """
        id_ = 'com.jiuyan.infashion:id/tv_title'
        return text_view.TextView(self.__item, id=id_).text

    def tap(self):
        """
            Summary:
                点击该item
        """
        log.logger.info("开始点击该tab")
        self.__item.click()
        log.logger.info("结束点击")


class TabList(base_frame_view.BaseFrameView):
    """
        Summary:
            Tab列表类
    """

    def __init__(self, parent, **kwargs):
        super(TabList, self).__init__(parent)
        self.__items = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__items:
            return [TabItem(item.parent, item) for item in self.__items]
        return None

#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 发布加工-玩字页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import view_pager

from gui_widgets.basic_widgets import linear_layout

from appium.webdriver import WebElement
import time


class PublishWordsArtActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布加工-玩字页

        Attributes:

    """
    name = '.publish.component.wordartformen.activity.PublishWordArtForMenActivity'

    def __init__(self, parent):
        super(PublishWordsArtActivity, self).__init__(parent)

        self._scroll_view = view_pager.ViewPager(self.parent, id='com.jiuyan.infashion:id/vp_word_art_for_men_viewpager')

    @property
    def tab_bar(self):
        """
            Summary:
                tab栏
        """

        return TabRecycler(self.parent)

    @property
    def word_art_list(self):
        """
            Summary:
                玩字模板列表
        Returns:

        """
        #  等待玩字页面贴纸元素加载完毕
        log.logger.info('等待玩字元素加载')
        if self.wait_for_element_present(
                self.base_parent,
                xpath='//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/rv_word_art_for_men\"]/'
                       'android.widget.LinearLayout'):
            log.logger.info('玩字元素已加载完毕')
            return linear_layout.LinearLayoutList(
                self.base_parent,
                xpath='//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/rv_word_art_for_men\"]/'
                      'android.widget.LinearLayout').layout_list
        log.logger.info("玩字元素加载失败")
        return None


    # *******************操作方法**************************


class TabRecycler(recycler_view.RecyclerView):

    def __init__(self, parent):
        super(TabRecycler, self).__init__(parent, type='android.support.v7.widget.RecyclerView')

    @property
    def tab_list(self):
        """
            Summary:
                搜索结果列表
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[1]/android.widget.RelativeLayout'
        return TabList(self.base_parent, xpath=xpath_).item_list

    @property
    def all_tab(self):
        """
            Summary:
                “全部”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="全部"]/..'
        return TabItem(self.base_parent, xpath=xpath_)

    @property
    def scenery_tab(self):
        """
            Summary:
                “风景”tab
        :return:
        """
        xpath_ = '//android.widget.TextView[@text="风景"]/..'
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
        id_ = 'com.jiuyan.infashion:id/tv_word_art_for_men_category_name'
        return text_view.TextView(self.__item, id=id_).text

    def tap(self):
        """
            Summary:
                点击该item
        """
        title_ = self.title
        log.logger.info("开始点击\"{}\"tab".format(title_))
        self.__item.click()
        log.logger.info("结束点击")
        time.sleep(4)


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

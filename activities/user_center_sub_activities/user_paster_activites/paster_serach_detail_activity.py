#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-贴纸搜索详情页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import list_view
from gui_widgets.custom_widgets import search_bar

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver import WebElement

import time


class PasterSearchDetailActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            贴纸搜索详情页，输入搜索文字后展开的面板

        Attributes:

    """

    def __init__(self, parent):
        super(PasterSearchDetailActivity, self).__init__(parent)

    @property
    def search_bar(self):
        """
            Summary:
                搜索栏
        """
        return search_bar.PasterSearchBar(self.parent, id='com.jiuyan.infashion:id/layout_search')

    @property
    def hot_search_title(self):
        """
            Summary:
                热门搜索标题
        """
        id_ = 'com.jiuyan.infashion:id/hot_search'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def hot_search_words(self):
        """
            Summary:
                搜索热词
        """
        id_ = 'com.jiuyan.infashion:id/tv_tag'
        return text_view.TextViewList(self.parent, id=id_).text_view_list

    @property
    def search_list_title(self):
        """
            Summary:
                搜索列表的标题：“最近搜索”\“搜索结果”\“in帮你找到XX个相关贴纸”
        """
        id_ = 'com.jiuyan.infashion:id/search_tip'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def search_list_view(self):
        """
            Summary:
                搜索结果列表模板
        """
        return PasterSearchListView(self.parent)


class PasterSearchListView(list_view.ListView):

    def __init__(self, parent):
        super(PasterSearchListView, self).__init__(parent, id='com.jiuyan.infashion:id/search_list')

    @property
    def item_list(self):
        """
            Summary:
                搜索结果列表
        """
        xpath_ = '//android.widget.ListView[1]/android.widget.LinearLayout'
        return SearchItemList(self.base_parent, xpath=xpath_).item_list


class SearchItem(base_frame_view.BaseFrameView):
    """
        Summary:
            搜索结果item类
    """
    ALERT_PASTER_ACTION = 1      # 弹出贴纸
    TO_SEARCH_RESULT_ACTION = 2  # 进入搜索结果页

    def __init__(self, parent, item=None, **kwargs):
        super(SearchItem, self).__init__(parent)
        self.__item = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def content(self):
        """
            Summary:
                推荐item的内容
        """
        id_ = 'com.jiuyan.infashion:id/name'
        return text_view.TextView(self.__item, id=id_).text

    @property
    def tag(self):
        """
            Summary:
                推荐item的分类标签
        """
        id_ = 'com.jiuyan.infashion:id/info'
        return text_view.TextView(self.__item, id=id_).text

    def tap(self, expected_action=1):
        """
            Summary:
                点击该item
            Args:
                expected_action:
                    1 ：期待贴纸弹出;
                    2 ：期待进入标题为“in帮你找到XX个相关贴纸”的搜索结果详情页
        """
        log.logger.info("开始点击该推荐内容")
        self.__item.click()
        log.logger.info("点击结束")
        if expected_action == self.ALERT_PASTER_ACTION:
            try:
                WebDriverWait(self.base_parent, 10).until(
                    EC.presence_of_element_located((MobileBy.ID, 'com.jiuyan.infashion:id/tv_dialog_sticker_name'))
                )
                log.logger.info("成功弹出贴纸对话框")
                return True
            except TimeoutException:
                log.logger.error("弹出贴纸对话框失败")
                return False
        elif expected_action == self.TO_SEARCH_RESULT_ACTION:
            try:
                WebDriverWait(self.base_parent, 10).until(
                    EC.text_to_be_present_in_element(
                        (MobileBy.ID, 'com.jiuyan.infashion:id/search_tip'), u'in帮你找到')
                )
                log.logger.info("成功进入搜索结果页")
                return True
            except TimeoutException:
                log.logger.error("进入搜索结果页失败")
                return False


class SearchItemList(base_frame_view.BaseFrameView):
    """
        Summary:
            搜索结果item列表类
    """

    def __init__(self, parent, **kwargs):
        super(SearchItemList, self).__init__(parent)
        self.__items = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__items:
            return [SearchItem(item.parent, item) for item in self.__items]
        return None



#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: IN主页-发现tab页面

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import edit_text
from gui_widgets.custom_widgets import search_bar

from activities import activities
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


class DiscoverTabActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            In主页面-发现tab

        Attributes:

    """
    name = '.InHomeActivity'

    def __init__(self, parent):
        super(DiscoverTabActivity, self).__init__(parent)
        self._scroll_view = recycler_view.RecyclerView(self.parent,
                                                        id='com.jiuyan.infashion:id/swipe_container')

    @property
    def broadcast_close_button(self):
        """
        允许通知遮罩的关闭按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/in_base_dialog_close'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def qr_code(self):
        """
            Summary:
                二维码扫一扫
        """
        id_ = 'com.jiuyan.infashion:id/layout_qrcode'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def search_box(self):
        """
            Summary:
                搜索框
        """
        id_ = 'com.jiuyan.infashion:id/search'
        return edit_text.EditText(self.parent, id=id_)

    @property
    def sign_up(self):
        """
            Summary:
                签到
        """
        id_ = 'com.jiuyan.infashion:id/layout_signup'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def hot_topic_icon(self):
        """
            Summary:
                热门话题箭头
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/layout_all_tag'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    # **************热门话题区域*******************************
    @property
    def hot_topic_recycler(self):
        """
            Summary:
                热门话题左右滑动区域
        """
        id_ = 'com.jiuyan.infashion:id/tag_recycler'
        return recycler_view.RecyclerView(self.parent, id=id_)

    @property
    def hot_topic_list(self):
        """
            Summary:
                热门话题列表
        """
        rec_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/tag_recycler')
        return HotTopicList(rec_, type='android.widget.RelativeLayout').topic_list

    # **********************图片/故事集/直播区域*************
    @property
    def square_head_bar(self):
        """
            Summary:
                图片/故事集/直播左右滑动栏
        """
        id_ = 'com.jiuyan.infashion:id/square_header_bar'
        return recycler_view.RecyclerView(self.parent, id=id_)

    @property
    def header_bar_more(self):
        """
            Summary:
                更多话题按钮
        Returns:

        """
        # id_ = 'com.jiuyan.infashion:id/square_header_bar_more' #com.jiuyan.infashion:id/square_header_more

        uiautomator_ = 'new UiSelector().resourceIdMatches("com.jiuyan.infashion:id/square_header_(bar_)?more")'
        return image_view.ImageView(self.parent, uiautomator=uiautomator_)

    @property
    def newest_header_tab(self):
        """
            Summary:
                head_bar里面最新tab
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains("最新")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    @property
    def hotest_header_tab(self):
        """
            Summary:
                head_bar里面最热tab
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains("最热")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    @property
    def square_item_list(self):
        """
            Summary:
                图片/故事集/直播九宫格列表
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/id_in_zan_animatorview'
        return SquareItemList(self.parent, id=id_).item_list

    @property
    def first_photo_item(self):
        """
            Summary:
                九宫格第一张图片
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/id_in_zan_animatorview'
        return SquareItemList(self.parent, id=id_).get_photo_item()

    @property
    def first_live_item(self):
        """
            Summary:
                九宫格第一张直播
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/id_in_zan_animatorview'
        return SquareItemList(self.parent, id=id_).get_live_item()

    @property
    def first_story_item(self):
        """
            Summary:
                九宫格第一张故事集
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/id_in_zan_animatorview'
        return SquareItemList(self.parent, id=id_).get_story_item()

    @property
    def ad_item(self):
        """
            Summary:
                广告
        Returns:

        """
        try:
            xpath_ = '//android.widget.TextView[@text="推广"]/..'
            return image_view.ImageView(self.base_parent, xpath=xpath_)
        except:
            return None

    # ************************引导遮罩***********************

    @property
    def double_click_guide(self):
        """
            Summary:
                双击点赞引导页
        """
        id_ = 'com.jiuyan.infashion:id/id_double_click'
        return image_view.ImageView(self.base_parent, id=id_)

    # ********************判断元素是否存在或已加载*********************

    def is_double_click_guide_mask_exist(self):
        """
            Summary:
                双击引导遮罩存在
        Returns:

        """
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/id_double_click', timeout=3):
            log.logger.info("双击引导遮罩存在")
            return True
        return False

    def is_square_item_exisit(self):
        """
            Summary:
                各tab下的九宫格加载是否成功
        Returns:

        """
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/id_in_zan_animatorview', timeout=3):
            log.logger.info("九宫格内容已加载完毕")
            return True
        log.logger.error("九宫格内容加载失败")
        return False

    # **************************搜索操作**************************
    def tap_search_box(self):
        """
            Summary:
                点击搜索框
        Returns:

        """
        log.logger.info("开始点击搜索框")
        self.search_box.tap()
        log.logger.info("完成搜索框点击")
        time.sleep(3)

    # ************************广告操作***************************
    def tap_ad(self):
        """
            Summary:
                点击广告
        Returns:

        """
        log.logger.info("开始点击广告")
        self.ad_item.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.WEBVIEW, 10):
            return True
        return False

    # ************************广场类操作***************************
    def tap_head_bar_more(self):
        """
            Summary:
                点击更多分类
        Returns:

        """
        log.logger.info("开始点击更多箭头")
        self.header_bar_more.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.SQUARE_CATEGORY, 10):
            return True
        return False

    # ************************话题操作***************************
    def tap_hot_topic_icon(self):
        """
            Summary:
                点击热门话题按钮
        Returns:

        """
        log.logger.info("开始点击热门话题按钮")
        self.hot_topic_icon.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.TOPIC_SQUARE, 10):
            log.logger.info("成功进入热门话题页")
            return True
        log.logger.error("进入热门话题页失败")
        return False

    def select_hot_topic(self, index=1):
        """
            Summary:
                选择热门话题
            Args:
                index:序号
        """
        log.logger.info("开始选择第{}个热门话题".format(index))
        status = self.hot_topic_list[index-1].tap()
        return status

    def swipe_topic_list(self, direction='right'):
        """
            Summary:
                左右滑动话题列表
            Args：
                direction: left:向左;right:向右
        """
        if direction == 'right':
            self.hot_topic_recycler.swipe_right_entire_recycler_view()
        elif direction == 'left':
            self.hot_topic_recycler.swipe_left_entire_recycler_view()
        else:
            log.logger.info("未指定方向")

    def remove_double_click_guide(self):
        """
            Summary:
                移除双击引导页
        Returns:

        """
        log.logger.info("开始点击双击点赞到引导")
        self.double_click_guide.tap()
        time.sleep(2)
        log.logger.info("完成结束引导到点击")

    #   重写向上滑动
    def swipe_up_entire_scroll_view(self, x=None):
        """
            Summary:
                向上滑动整个scroll view的高度

        """
        location = self._scroll_view.location
        size = self._scroll_view.size
        x = x or location['x'] + size['width']/3
        start_y = location['y'] + size['height'] - 1
        end_y = location['y'] + 1

        log.logger.info("开始向上滑动整个可滑动区域的屏幕")
        self.swipe_up(x, start_y, end_y)
        log.logger.info("向上滑动结束")
        time.sleep(2)


class HotTopic(base_frame_view.BaseFrameView):

    def __init__(self, parent, item=None, **kwargs):
        super(HotTopic, self).__init__(parent)
        self.__item = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def title(self):

        return text_view.TextView(self.__item, id='com.jiuyan.infashion:id/tv_title').text

    def tap(self):

        log.logger.info("开始点击该话题")
        title = self.title
        self.__item.click()
        if self.base_parent.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功进入话题\"{}\"的详情页".format(title))
            return True
        log.logger.error("进入话题详情页失败")
        return False


class HotTopicList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(HotTopicList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def topic_list(self):

        if self.__item_list:
            return [HotTopic(item.parent, item) for item in self.__item_list]
        return None


class SquareItem(base_frame_view.BaseFrameView):

    """
        Summary:
            图片/直播/故事集广场九宫格元素
    """
    def __init__(self, parent, item=None, **kwargs):
        super(SquareItem, self).__init__(parent)
        self.__item = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def story_icon(self):
        id_ = 'com.jiuyan.infashion:id/iv_story'
        return image_view.ImageView(self.__item, id=id_)

    @property
    def live_icon(self):
        id_ = 'com.jiuyan.infashion:id/iv_live'
        return image_view.ImageView(self.__item, id=id_)

    def tap(self):

        type_dic = {
            'story': '故事集',
            'live': '直播',
            'photo': '图片'
        }
        type_ = self.get_type()

        log.logger.info("开始点击该{}方块".format(type_dic[type_]))
        self.__item.click()
        if self.wait_one_of_activities((activities.ActivityNames.FRIEND_PHOTO_RECOMMEND_DETAIL,
                                        activities.ActivityNames.STORY_DETAIL,
                                        activities.ActivityNames.LIVE), 10):
            log.logger.info("成功进入详情页")
            return True
        log.logger.error("进入详情页失败")
        return False

    def get_type(self):
        """
            Summary:
                获取该九宫格的类型
        Returns:

        """
        if self.wait_for_element_present(self.__item, timeout=1, id='com.jiuyan.infashion:id/iv_story'):
            return 'story'
        if self.wait_for_element_present(self.__item, timeout=1, id='com.jiuyan.infashion:id/iv_live'):
            return 'live'
        return 'photo'


class SquareItemList(base_frame_view.BaseFrameView):
    """
        Summary:
            图片/直播/故事集广场九宫格元素列表
    """

    def __init__(self, parent, **kwargs):
        super(SquareItemList, self).__init__(parent)
        self.__item_list = None

        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/id_in_zan_animatorview'):
            self.__item_list = self.find_elements(**kwargs)
        else:
            log.logger.error("该tab下九宫格未初始化完毕")
            raise

    @property
    def item_list(self):

        if self.__item_list:
            return [SquareItem(item.parent, item) for item in self.__item_list]
        return None

    def get_story_item(self):
        """
            Summary:
                获取第一个故事集九宫格
        Returns:

        """
        for item in self.__item_list:
            if self.wait_for_element_present(item, timeout=2, id='com.jiuyan.infashion:id/iv_story'):
                return SquareItem(item.parent, item)
        return None

    def get_live_item(self):
        """
            Summary:
                获取第一个故事集九宫格
            Returns:
        """
        for item in self.__item_list:
            if self.wait_for_element_present(item, timeout=2, id='com.jiuyan.infashion:id/iv_live'):
                return SquareItem(item.parent, item)
        return None

    def get_photo_item(self):
        """
            Summary:
                获取第一个照片九宫格
            Returns:
        """
        for item in self.__item_list:
            if not self.wait_for_element_present(item, timeout=1, id='com.jiuyan.infashion:id/iv_live') and \
                    not self.wait_for_element_present(item, timeout=1, id='com.jiuyan.infashion:id/iv_story'):
                return SquareItem(item.parent, item)
        return None


class SearchPage(base_frame_view.BaseFrameView):
    """
        Summary:
            点击发现页的搜索框后进入到的搜索页
    """
    def __init__(self, parent):
        super(SearchPage, self).__init__(parent)

    @property
    def top_search_bar(self):
        """
            Summary:
                顶部搜索栏
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/layout_search_area'
        return search_bar.SearchBar(self.parent, id=id_)

    @property
    def user_tab(self):
        """
            Summary:
                用户tab
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_search_user'
        return text_view.TextView(self.parent, id=id_)

    @property
    def tag_tab(self):
        """
            Summary:
                标签tab
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_search_user'
        return text_view.TextView(self.parent, id=id_)

    @property
    def user_list(self):
        """
            Summary:
                用户搜索结果列表
        Returns:

        """
        xpath_ = '//android.widget.ListView[@resource-id="com.jiuyan.infashion:id/lv_search_result"]/' \
                 'android.widget.RelativeLayout'
        return UserItemList(self.parent, xpath=xpath_).user_list

    @property
    def tag_list(self):
        """
            Summary:
                话题列表
        Returns:

        """
        xpath_ = '//android.widget.ListView[@resource-id="com.jiuyan.infashion:id/lv_search_result"]/' \
                 'android.widget.RelativeLayout'
        return TagItemList(self.parent, xpath=xpath_).tag_list

    # ****************操作方法*******************

    def tap_user_tab(self):
        """
            Summary:
                点击用户tab
        Returns:

        """
        log.logger.info("开始点击用户tab")
        self.user_tab.tap()
        log.logger.info("点击用户tab完毕")
        time.sleep(3)

    def tap_tag_tab(self):
        """
            Summary:
                点击标签tab
        Returns:

        """
        log.logger.info("开始点击标签tab")
        self.tag_tab.tap()
        log.logger.info("点击标签tab完毕")
        time.sleep(3)

    def is_search_result_exist(self):
        """
            Summary:
                验证有搜索结果
        Returns:

        """
        if self.wait_for_element_present(self.base_parent, id='com.jiuyan.infashion:id/lv_search_result'):
            log.logger.info("已有搜索结果")
            return True
        log.logger.error("搜索结果没出现")
        return False


class UserItem(base_frame_view.BaseFrameView):
    """
        Summary:
            用户搜索结果
    """
    def __init__(self, parent, item=None, **kwargs):
        super(UserItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def user_avatar(self):
        """
            Summary:
                用户头像
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def name(self):
        """
            Summary:
                用户名称
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def in_id(self):
        """
            Summary:
                in号
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_info'
        return text_view.TextView(self._layout_view, id=id_)

    #************************操作方法**************************

    def tap(self):
        """
            Summary:
                点击头像
        Returns:

        """
        name = self.name
        log.logger.info("开始点击用户\"{}\"".format(name))
        self._layout_view.click()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入个人信息in记页")
            return True
        log.logger.error("进入个人信息in记页失败")
        return False


class UserItemList(base_frame_view.BaseFrameView):
    """
        Summary:
            用户动态卡片类列表
    """
    def __init__(self, parent, **kwargs):
        super(UserItemList, self).__init__(parent)
        self._item_list = self.find_elements(**kwargs)

    @property
    def user_list(self):

        if self._item_list:
            return [UserItem(item.parent, item) for item in self._item_list]
        return None


class TagItem(base_frame_view.BaseFrameView):
    """
        Summary:
            标签搜索结果
    """
    def __init__(self, parent, item=None, **kwargs):
        super(TagItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def tag_name(self):
        """
            Summary:
                标签名称
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def info(self):
        """
            Summary:
                已有XX张照片
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_info'
        return text_view.TextView(self._layout_view, id=id_)

    #************************操作方法**************************

    def tap(self):
        """
            Summary:
                点击头像
        Returns:

        """
        name = self.name
        log.logger.info("开始点击用户\"{}\"".format(name))
        self._layout_view.click()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.TOPIC_DETAIL, 10):
            log.logger.info("成功进入话题详情页")
            return True
        log.logger.error("进入话题详情页失败")
        return False


class TagItemList(base_frame_view.BaseFrameView):
    """
        Summary:
            用户动态卡片类列表
    """
    def __init__(self, parent, **kwargs):
        super(TagItemList, self).__init__(parent)
        self._item_list = self.find_elements(**kwargs)

    @property
    def tag_list(self):

        if self._item_list:
            return [UserItem(item.parent, item) for item in self._item_list]
        return None


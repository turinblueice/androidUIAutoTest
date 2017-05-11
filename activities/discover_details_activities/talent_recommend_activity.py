#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:达人推荐详情页

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
from gui_widgets.basic_widgets import radio_button

from appium.webdriver import WebElement
from appium.webdriver.common import touch_action
from selenium.webdriver.common.touch_actions import TouchActions
from activities import activities

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TalentRecommendActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            达人推荐页面

        Attributes:

    """
    name = '.module.square.activity.EretarActivity'  # 裁剪图片activity名称

    def __init__(self, parent):
        super(TalentRecommendActivity, self).__init__(parent)

        #  等待初始化
        self.wait_for_element_present(self.base_parent, id='com.jiuyan.infashion:id/login_tv_title')

        self._scroll_view = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/square_rv_tag')

    @property
    def talent_recommend(self):
        """
            Summary:
                达人推荐按钮
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_title'
        return text_view.TextView(self.parent, id=id_)

    @property
    def talent_apply(self):
        """
            Summary:
                申请达人按钮
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_title_right'
        return text_view.TextView(self.parent, id=id_)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = 'com.jiuyan.infashion:id/login_tv_title_left'
        return text_view.TextView(self.parent, id=id_)

    @property
    def talent_list(self):
        """
            Summary:
                达人列表
        :return:
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/square_rv_tag"]/' \
                 'android.widget.LinearLayout'
        return TalentContainerList(self.base_parent, xpath=xpath_).item_list

    @property
    def category_list(self):
        """
            Summary:
                种类列表
        :return:
        """
        xpath_ = '//android.widget.ListView[@resource-id="com.jiuyan.infashion:id/square_rv_menu"]/' \
                 'android.widget.LinearLayout'
        return TalentCategoryList(self.base_parent, xpath=xpath_).item_list

    # **************************操作方法*****************************
    def wait_for_talent(self, timeout=10):
        """
            Summary:
                显示等待达人加载完毕
        :return:
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/square_rv_tag"]/' \
                 'android.widget.LinearLayout'
        if self.wait_for_element_present(self.base_parent, timeout=timeout, xpath=xpath_):
            log.logger.info("达人列表已记载")
            return True
        log.logger.error("达人列表加载失败")
        return False

    def tap_back_button(self):
        """
            Summary:
                点击返回按钮
        """
        log.logger.info("开始点击返回按钮")
        self.back_button.tap()
        log.logger.info("完成返回按钮点击")
        if self.wait_activity(activities.ActivityNames.SQUARE_CATEGORY, 10):
            log.logger.info("成功返回到话题分类页面")
            return True
        log.logger.error("返回失败")
        return False


class TalentContainer(base_frame_view.BaseFrameView):
    """
        Summary:
            达人推荐
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(TalentContainer, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self._index = index
        self._xpath = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/square_rv_tag"]/' \
                      'android.widget.LinearLayout[{}]'.format(self._index+1)


    @property
    def talent_name(self):
        """
            Summary:
                达人姓名
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_name'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def talent_avatar(self):
        """
            Summary:
                达人头像
        """
        id_ = 'com.jiuyan.infashion:id/transition_avatar_id'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def follow_button(self):
        """
            Summary:
                关注按钮
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_attention'
        return radio_button.RadioButton(self._layout_view, id=id_)

    @property
    def image_list(self):
        """
            Summary:
                图片列表
        """
        return image_view.ImageViewList(self._layout_view, id='com.jiuyan.infashion:id/login_iv_pic').image_list

    # ********************操作方法*************************

    def tap_avatar(self):
        """
            Summary:
                点击头像

        """
        curr_name = self.talent_name
        log.logger.info("开始点击\"{}\"的头像".format(curr_name))
        self.talent_avatar.tap()
        log.logger.info("点击完毕")
        if self.base_parent.wait_activity(activities.ActivityNames.DIARY_INFO, 10):
            log.logger.info("成功进入好友in记页面")
            return True
        log.logger.error("进入好友in记页面失败")
        return False

    def tap_image(self, index):
        """
            点击图片
        Args:
            index:
                图片序号
        Returns:

        """
        log.logger.info("点击第{}张".format(index+1))
        self.image_list[index].tap()
        log.logger.info("完成点击")
        if self.base_parent.wait_activity(activities.ActivityNames.FRIEND_PHOTO_DETAIL, 10):
            log.logger.info("成功进入好友照片页面")
            return True
        log.logger.error("进入好友照片页面失败")
        return False

    def tap_follow_button(self):
        """
            Summary:
                点击关注按钮
        """
        log.logger.info("开始点击关注")
        self.follow_button.tap()
        time.sleep(2)
        log.logger.info("点击完毕")
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.element_located_to_be_selected(
                    (MobileBy.XPATH, self._xpath+'/android.widget.RelativeLayout[1]/android.widget.RadioButton[1]')
                )
            )
            return True
        except:
            return False


class TalentContainerList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(TalentContainerList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [TalentContainer(item.parent, item, index) for index, item in enumerate(self.__list)]
        return None


class TalentCategory(base_frame_view.BaseFrameView):
    """
        Summary:
            达人分类
    """
    def __init__(self, parent, item=None, **kwargs):
        super(TalentCategory, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)

    @property
    def title(self):
        """
            Summary:
                达人分类的名称
        """
        id_ = 'com.jiuyan.infashion:id/square_tv_tag_menu'
        return text_view.TextView(self._layout_view, id=id_).text

    # ********************操作方法*************************

    def tap(self):
        """
            Summary:
                点击分类
        """
        title_ = self.title
        log.logger.info("开始点击\"{}\"".format(title_))
        self._layout_view.click()
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/square_rv_tag"]/' \
                 'android.widget.LinearLayout'
        if self.wait_for_element_present(self.base_parent, xpath=xpath_):
            # 点击左侧不同的达人类别后,等待右侧达人初始化加载
            log.logger.info("\"{}\"的达人已加载成功".format(title_))
            return True
        log.logger.error("达人列表初始化失败")
        return False


class TalentCategoryList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(TalentCategoryList, self).__init__(parent)
        self.__list = self.find_elements(**kwargs)

    @property
    def item_list(self):

        if self.__list:
            return [TalentCategory(item.parent, item) for item in self.__list]
        return None

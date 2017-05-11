#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 图片发布加工页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import view
from gui_widgets.basic_widgets import seek_bar

from gui_widgets.custom_widgets import save_popup_window

from activities import activities

from appium.webdriver import WebElement

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class PublishCoreActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            图片发布加工页

        Attributes:

    """
    name = '.publish.PublishCoreActivity'

    def __init__(self, parent):
        super(PublishCoreActivity, self).__init__(parent)
        self._layout_view = self.find_element(id='com.jiuyan.infashion:id/rl_publish_core')

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_publish_core_previous'
        return text_view.TextView(self.parent, id=id_)

    @property
    def photo_available_list(self):
        """
            Summary:
                顶栏图片列表
        """
        if self.wait_for_element_present(parent=self.base_parent, id='com.jiuyan.infashion:id/hrv_publish_thumbnail'):
            recycler_view_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/hrv_publish_thumbnail')
            return PhotoItemList(recycler_view_, type='android.widget.FrameLayout').item_list
        return None

    @property
    def finish_button(self):
        """
            Summary:
                完成按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_publish_core_next'
        return text_view.TextView(self.parent, id=id_)

    @property
    def add_photo_thumb_button(self):
        """
            Summary:
                添加照片按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_add_one'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def photo_bar_hide_display_button(self):
        """
            Summary:
                照片栏隐藏/显示按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_publish_toolbar_hide'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def guide_mask(self):
        """
            Summary:
                引导遮罩
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/rl_guide_for_women'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    # ***************************底部工具***************************
    @property
    def paster_button(self):
        """
            Summary:
                贴纸工具
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains(\"贴纸\")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    @property
    def filter_button(self):
        """
            Summary:
                滤镜工具
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains(\"滤镜\")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    @property
    def mark_tool(self):
        """
            Summary:
                标签工具
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains(\"标签\")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    @property
    def character_tool(self):
        """
            Summary:
                玩字工具
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains(\"玩字\")'
        return text_view.TextView(self.parent, uiautomator=uiautomator_)

    # ************************点击滤镜出现的元素***********************
    @property
    def filter_bar(self):
        """
            Summary:
                滤镜效果栏
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/hrv_publish_filter'
        return recycler_view.RecyclerView(self.parent, id=id_)

    @property
    def filter_effect_choice_list(self):
        """
            Summary:
                滤镜效果选项框
        Returns:

        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id=\"com.jiuyan.infashion:id/hrv_publish_filter\"]/' \
                 'android.widget.LinearLayout'

        return FilterChoiceItemList(self.base_parent, xpath=xpath_).item_list

    @property
    def filter_seek_bar(self):
        """
            Summary:
                滤镜效果调整栏
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/sb_publish_filter_ratio'
        return seek_bar.SeekBar(self.parent, id=id_)

    @property
    def beauty_button(self):
        """
            Summary:
                一健美颜按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/spv_publish_filter_beauty'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def beauty_level_button(self):
        """
            Summary:
                美颜强度按钮,点击一健美颜按钮会出现
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/pb_level'
        return view.View(self.parent, id=id_)

    @property
    def beauty_level_choices_list(self):
        """
            Summary:
                美颜强度选项列表
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches(\"com.jiuyan.infashion:id/btn_level_.+\")'
        return view.ViewList(self.parent, uiautomator=uiautomator_).view_list

    # ************************点击标签出现的元素***********************

    @property
    def words_tag(self):
        """
            Summary:
                文字标签
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_publish_entry_tag_status'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def brand_tag(self):
        """
            Summary:
                品牌标签
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_publish_entry_tag_brand'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def address_tag(self):
        """
            Summary:
                地点标签
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/iv_publish_entry_tag_address'
        return image_view.ImageView(self.parent, id=id_)

    # **************************操作方法******************************

    def tap_back_button(self, save=True, cancel=False):
        """
            Summary:
                点击左上角返回按钮
            Args:
                save:True:临时保存;False:不保存
                cancel:点击取消
        """
        log.logger.info("点击左上角返回按钮")
        self.back_button.tap()
        log.logger.info("完成返回按钮点击")
        if self.wait_for_element_present(self.parent, id='com.jiuyan.infashion:id/publish_menu_save_tmp_confirm'):
            log.logger.info('成功吊起保存面板')
            popup_window = save_popup_window.SavePopupWindow(self.parent)
            if not cancel:
                if save:
                    status = popup_window.tap_save_temporary_button()
                else:
                    status = popup_window.tap_no_save_button()
                return status
            log.logger.info("点击取消")
            popup_window.tap_cancel_button()
            return True
        log.logger.error("没有吊起保存面板")
        return False

    def is_guide_mask_exist(self):
        """
            Summary:
                判断引导遮罩是否存在
        Returns:

        """
        if self.wait_for_element_present(self.parent, timeout=3, id='com.jiuyan.infashion:id/rl_guide_for_women'):
            log.logger.info("存在引导遮罩")
            return True
        return False

    def is_sticker_mask_exist(self):
        """
            Summary:
                判断魔法棒引导遮罩
        Returns:

        """
        if self.wait_for_element_present(self.parent, timeout=3, id='com.jiuyan.infashion:id/ll_magic_guide'):
            log.logger.info("存在魔法棒遮罩")
            return True
        return False

    def remove_guide_mask(self):
        """
            Summary:
                消除引导遮罩
        Returns:

        """
        log.logger.info("点击引导遮罩")
        self.tap_window_center()
        log.logger.info("完成点击")
        time.sleep(3)

    def tap_finish_button(self):
        """
            Summray:
                点击完成按钮
        """
        log.logger.info("开始点击完成按钮")
        self.finish_button.tap()
        log.logger.info("结束完成按钮点击")
        if self.wait_activity(activities.ActivityNames.PUBLISH, 10):
            log.logger.info("成功进入发布页")
            return True
        log.logger.error("进入发布页失败")
        return False

    def tap_add_photo_button(self):
        """
            Summary:
                点击添加图片按钮
        Returns:

        """
        log.logger.info("点击添加照片按钮")
        self.add_photo_thumb_button.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
            log.logger.info("成功进入图片选择页")
            return True
        log.logger.error("进入图片选择页面失败")
        return False

    # *************滤镜操作**********
    def tap_paster_button(self):
        """
            Summary:
                点击贴纸按钮
        Returns:

        """
        log.logger.info("开始点击贴纸按钮")
        self.paster_button.tap()
        log.logger.info("完成贴纸按钮的点击")
        if self.wait_activity(activities.ActivityNames.PASTER_MALL, 10):
            log.logger.info("成功进入贴纸商城")
            return True
        log.logger.error("进入贴纸商城失败")
        return False

    # *************滤镜操作**********
    def tap_filter_button(self):
        """
            Summary:
                点击滤镜按钮
        Returns:

        """
        log.logger.info("开始点击滤镜按钮")
        self.filter_button.tap()
        log.logger.info("完成滤镜按钮的点击")
        if self.wait_for_element_present(self.parent, timeout=3, id='com.jiuyan.infashion:id/fl_filter_bar'):
            log.logger.info('成功吊起滤镜工具栏')
            return True
        log.logger.error("吊起滤镜工具栏失败")
        return False

    def tap_beauty_button(self):
        """
            Summary:
                点击一键美颜按钮
        Returns:

        """
        log.logger.info("开始点击一健美颜按钮")
        self.beauty_button.tap()
        log.logger.info("完成一健美颜按钮的点击")
        if self.wait_for_element_present(self.parent, timeout=3, id='com.jiuyan.infashion:id/rl_root'):
            log.logger.info("美颜强度框出现")
            return True
        log.logger.error("美艳强度框没出现")
        return False

    def select_beauty_level(self, level=0):
        """
            Summary:
                　选择美颜强度
        Args:
            level:
                0,1,2,3,4
        Returns:

        """
        log.logger.info("选择美颜强度{}".format(level))
        self.beauty_level_choices_list[level].tap()
        log.logger.info("完成美颜强度的选择")
        time.sleep(3)

    def tap_beauty_level(self):
        """
            Summary:
                点击美颜强度按钮
        Returns:

        """
        uiautomator_ = 'new UiSelector().resourceIdMatches(\"com.jiuyan.infashion:id/btn_level_.+\")'
        log.logger.info("开始点击美颜强度按钮")
        self.beauty_level_button.tap()
        log.logger.info("完成美颜强度按钮的点击")
        time.sleep(3)
        if not self.wait_for_element_present(self.parent, timeout=3, uiautomator=uiautomator_):
            log.logger.info("美颜强度框消失")
            return True
        log.logger.error("美艳强度框依然存在")
        return False

    def is_seek_bar_exist(self):
        """
            Summary:
                滤镜效果调整栏是否出现
        Returns:

        """
        if self.wait_for_element_present(self.parent, timeout=5, id='com.jiuyan.infashion:id/sb_publish_filter_ratio'):
            log.logger.info('滤镜效果栏存在')
            return True
        log.logger.error("滤镜效果栏不存在")
        return False

    def is_seek_bar_not_exist(self):
        """
            Summary:
                滤镜效果调整栏是否出现
        Returns:

        """
        if self.wait_for_element_disappear(self.parent, timeout=8, id='com.jiuyan.infashion:id/sb_publish_filter_ratio'):
            log.logger.info('滤镜效果栏已消失')
            return True
        log.logger.error("滤镜效果栏未消失")
        return False

    def is_no_filter_effect_displayed(self):
        """
            Summary:
                无滤镜效果选项是否在可视区域
        Returns:

        """
        uiautomator_ = 'new UiSelector().textContains(\"无\")'
        if self.wait_for_element_present(timeout=2, uiautomator=uiautomator_):
            return True
        return False

    # *************标签操作**********
    def tap_mark_tool(self):
        """
            Summary:
                点击标签工具
        Returns:

        """
        log.logger.info("开始点击标签工具")
        self.mark_tool.tap()
        log.logger.info('完成标签工具点击')
        if self.wait_for_element_present(timeout=3, id='com.jiuyan.infashion:id/iv_publish_entry_tag_status'):
            return True
        return False

    def tap_words_tag(self):
        """
            Summary:
                点击文字标签
        Returns:

        """
        log.logger.info('点击文字标签')
        self.words_tag.tap()
        log.logger.info('文字标签点击完毕')
        if self.wait_activity(activities.ActivityNames.PUBLISH_TAG, 5):
            log.logger.info('成功进入发布标签页')
            return True
        log.logger.error('进入标签页失败')
        return False

    # *************玩字操作**********

    def tap_character_button(self):
        """
            Summary:
                点击玩字按钮
        Returns:

        """
        log.logger.info("开始点击玩字按钮")
        self.character_tool.tap()
        log.logger.info("结束玩字按钮点击")
        if self.wait_activity(activities.ActivityNames.PUBLISH_WORDS, 10):
            log.logger.info("成功进入玩字页面")
            return True
        log.logger.error("进入玩字页面失败")
        return False

    def make_words_art_popup_appearance(self):
        """
            Summary:
                呼出玩字的底部遮罩, 目前只测试过支持风景类型的遮罩
        Returns:

        """
        log.logger.info("点击屏幕玩字区域,呼出底部遮罩")

        window_size = self.base_parent.get_window_size()
        x = window_size['width']/3
        y = window_size['height']/5

        log.logger.info("为呼出玩字遮罩,点击屏幕坐标({},{})".format(x, y))
        self.base_parent.tap([(x, y)])
        while not self.wait_for_element_present(self.base_parent, timeout=3,
                                                id='com.jiuyan.infashion:id/publish_art_text_inputview'):
            y += 20
            if y > window_size['height']:
                log.logger.error("呼出玩字遮罩失败")
                return False
            log.logger.info("玩字遮罩未出现,点击屏幕坐标({},{})".format(x, y))
            self.base_parent.tap([(x, y)])
        log.logger.info('玩字遮罩已呼出')
        return True


class PhotoItem(base_frame_view.BaseFrameView):
    """
        Summary:
            照片item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(PhotoItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__is_select = True
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    @property
    def is_selected(self):

        return self.__is_select

    def tap(self):
        """
            Summary:
                点击该图片
        """
        log.logger.info("开始点击选择{}照片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self._layout_view.click()
        time.sleep(2)
        log.logger.info("点击完毕")

    # def select(self):
    #     """
    #         Summary:
    #             选择图片，点击图片区域即可选择，无需点击check_box
    #     """
    #     if not self.__is_select:
    #         log.logger.info("开始点击选择{}图片".format('第'+str(self.__index)+'张' if self.__index is not None else '该'))
    #         self._layout_view.click()
    #         time.sleep(2)
    #         self.__is_select = True
    #         log.logger.info("已完成图片选择")

    def unselect(self):
        """
            Summary:
                取消选择图片
        """
        if self.__is_select:
            log.logger.info("开始取消选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
            self._layout_view.click()
            time.sleep(3)
            self.__is_select = False
            log.logger.info("已完成图片取消选择")


class PhotoItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PhotoItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            log.logger.info("可视区域内图片个数为{}".format(len(self.__item_list)))
            return [PhotoItem(item.parent, item, index) for index, item in enumerate(self.__item_list, start=1)]
        return None

# ***************************************滤镜效果选项列表类*************************************


class FilterChoiceItem(base_frame_view.BaseFrameView):
    """
        Summary:
            滤镜效果选项
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(FilterChoiceItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__is_select = True
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    @property
    def name(self):
        """
            Summary:
                滤镜选项名称
        Returns:

        """
        return text_view.TextView(self._layout_view, id='com.jiuyan.infashion:id/tv_photo_filter_name').text

    @property
    def is_selected(self):

        name = self.name
        if self.wait_for_element_present(id='com.jiuyan.infashion:id/riv_photo_filter_cover'):
            log.logger.info("\"{}\"被选中".format(name))
            return True
        return False

    def select(self):
        """
            Summary:
                点击该效果
        """
        name = self.name
        log.logger.info("开始点击{}效果".format('第' + str(self.__index) + '个' if self.__index is not None else '该'))
        log.logger.info("点击\"{}\"".format(name))
        self._layout_view.click()
        log.logger.info("点击完毕")
        time.sleep(3)


class FilterChoiceItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(FilterChoiceItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            log.logger.info("可视区域内滤镜效果个数为{}".format(len(self.__item_list)))
            return [FilterChoiceItem(item.parent, item, index) for index, item in enumerate(self.__item_list, start=1)]
        return None

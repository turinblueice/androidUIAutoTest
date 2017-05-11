#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 选择图片上传页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_button
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import image_view

from gui_widgets.custom_widgets import alert
from appium.webdriver import WebElement
from activities import activities

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time


class StoryGalleryActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发图-选择图片/写故事页面

        Attributes:

    """
    name = '.album.StoryGalleryActivity'
    STORY_PHOTO = 'photo_list'
    STORY_SELECT_ALL = 'all_button'
    
    def __init__(self, parent):
        super(StoryGalleryActivity, self).__init__(parent)
        self._layout_view = frame_layout.FrameLayout(self.parent, type='android.widget.FrameLayout')

    @property
    def photo_tab(self):
        """
            Summary:
                发图片tab按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/bottom_left'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def story_tab(self):
        """
            Summary:
                写故事tab按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/bottom_right'
        return relative_layout.RelativeLayout(self.parent, id=id_)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = "com.jiuyan.infashion:id/back"
        return button.Button(self.parent, id=id_)

    @property
    def album_drop_list_button(self):
        """
            Summary:
                相册下拉列表按钮-相机胶卷
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/album'
        return text_view.TextView(self.parent, id=id_)

    @property
    def album_title(self):
        """
            Summary:
                相册集的名称
        """
        id_ = 'com.jiuyan.infashion:id/pic_text'
        return text_view.TextView(self.parent, id=id_).text

    @property
    def next_step_button(self):
        """
            Summary:
                下一步按钮
        """
        id_ = "com.jiuyan.infashion:id/next"
        return text_view.TextView(self.parent, id=id_)

    @property
    def selected_photo_count(self):
        """
            Summary:
                选择的图片数量
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/count'
        return text_view.TextView(self.parent, id=id_).text

    # *************************"发图片"tab下的属性******************************

    # 2.9.9版本该页面已没有
    # @property
    # def camera(self):
    #     """
    #         Summary:
    #             相机按钮
    #     """
    #     recycler_view_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/gallery_list')
    #
    #     #  列表下首个id为item_photo_root的元素为摄像头
    #     return frame_layout.FrameLayout(recycler_view_, id='com.jiuyan.infashion:id/item_photo_root')

    @property
    def image_photo_list(self):
        """
            Summary:
                发图片tab下，要上传的图片列表
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/gallery_list"]/' \
                 'android.widget.RelativeLayout'

        #  等待图片列表全部载入，载入首张图片即可认为列表已初始化完毕
        self.wait_for_element_present(id='com.jiuyan.infashion:id/item_photo_image')
        return PostImgItemList(self.base_parent, xpath=xpath_).item_list

    @property
    def image_photo_enable_picked_count(self):
        """
            Summary:
                屏幕内可选图片数量
        :return:
        """
        all_count = len(self.image_photo_list)
        return all_count if all_count <= 11 else 11  # 单个屏幕中最多可显示可点击图片为11张

    # ************************写故事tab下的元素***************
    @property
    def story_tab_in_diary_album_bar(self):
        """
            Summary:
                写故事tab下，展开下拉列表后，in记相册栏
        """
        recycler_view_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/gallery_menu')
        return relative_layout.RelativeLayout(recycler_view_, type='android.widget.RelativeLayout')

    @property
    def story_tab_album_bar_list(self):
        """
            Summary:
                写故事tab下，展开下拉列表后的相册列表
        """
        recycler_view_ = recycler_view.RecyclerView(self.parent, id='com.jiuyan.infashion:id/gallery_menu')
        return relative_layout.RelativeLayoutList(
            recycler_view_, type='android.widget.RelativeLayout').relative_layout_list

    @property
    def story_photo_list_dictionary(self):
        """
            Summary:
                写故事tab下，要上传的图片列表，格式为
                {
                    "2016年07月25日":{
                                        'select_all_button':button,
                                        'photo_list':[relative_layout, relative_layout]
                                    },
                    "2016年07月26日":{
                                        'select_all_button':button,
                                        'photo_list':[relative_layout, relative_layout, ...]
                                    }
                }
        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/story_list"]/' \
                 'android.widget.RelativeLayout'
        all_relative_list = relative_layout.RelativeLayoutList(self.base_parent, xpath=xpath_).relative_layout_list

        all_date_photo_dic = dict()  # 所有日期的照片列表
        tmp_date = None
        for relative_item in all_relative_list:
            try:
                tmp_date = text_view.TextView(relative_item, id='com.jiuyan.infashion:id/story_item_date').text
                all_date_photo_dic[tmp_date] = dict()
                all_date_photo_dic[tmp_date][self.STORY_SELECT_ALL] = text_view.TextView(
                    relative_item, id='com.jiuyan.infashion:id/story_item_sel')
                all_date_photo_dic[tmp_date][self.STORY_PHOTO] = list()
            except NoSuchElementException:
                if tmp_date:
                    web_element = relative_item.get_webelement()
                    index = len(all_date_photo_dic[tmp_date]['photo_list'])
                    log.logger.info('当前图片为{}的第{}张图片'.format(tmp_date, index+1))
                    all_date_photo_dic[tmp_date][self.STORY_PHOTO].append(
                        PostImgItem(relative_item.parent, web_element, index+1))

        return all_date_photo_dic

    @property
    def date_photo_albums(self):
        """
            Summary:
                按时间划分的相册列表
            Return:
                [
                    ("2016年07月25日", {
                                        'select_all_button':button,
                                        'photo_list':[relative_layout, relative_layout]
                                    }),
                    ("2016年07月26日",{
                                        'select_all_button':button,
                                        'photo_list':[relative_layout, relative_layout, ...]
                                    })
                ]
        """
        return self.story_photo_list_dictionary.items()

    @property
    def in_diary_photo_list(self):
        """
            Summary:
                "in记"相册下的所有照片列表,其他相册则使用"日期":{"全选按钮"：button,"相册列表":[]}的方式
        """
        id_ = 'com.jiuyan.infashion:id/item_photo_root'
        return PostImgItemList(self.parent, id=id_).item_list

    # ************************操作***************************
    def open_camera(self):
        """
            Summary:
                打开摄像头
        """
        log.logger.info("点击打开摄像头")
        self.camera.tap()
        log.logger.info("摄像头已打开")
        if self.wait_for_system_alert(timeout=3):
            curr_alert = alert.PhoneSystemAlert(self.parent)
            log.logger.info("系统提示框勾选")
            try:
                if curr_alert.checkbox.is_displayed():
                    log.logger.info('勾选提示框的复选框')
                    curr_alert.checkbox.tap()
            except:
                pass
            curr_alert.confirm_button.tap()

        if self.wait_activity(activities.ActivityNames.STORY_CAMERA, 10):
            log.logger.info("成功进入拍照故事编辑页")
            return True
        log.logger.error("进入拍照故事编辑页失败")
        return False

    def select_image_photo(self, index):
        """
            Summary:
                选择发图片tab下要上传的图片
            Args:
                index: 图片序号
        """
        self.image_photo_list[index-1].select()
        time.sleep(1)

    def unselect_image_photo(self, index):
        """
            Summary:
                取消选择发图片tab下上传的图片
            Args:
                index: 图片序号
        """
        self.image_photo_list[index-1].unselect()
        time.sleep(1)

    def tap_photo_next_step_button(self, timeout=10):
        """
            Summary:
                点击继续按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击下一步按钮")
        self.next_step_button.tap()
        time.sleep(5)
        if self.wait_activity(activities.ActivityNames.PUBLISH_CORE, timeout):
            log.logger.info("成功进入发布加工页")
            return True
        log.logger.error("进入发布加工失败")
        return False

    def tap_story_next_step_button(self, timeout=10):
        """
            Summary:
                点击继续按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击下一步按钮")
        self.next_step_button.tap()
        if self.wait_activity(activities.ActivityNames.STORY_EDIT, timeout):
            log.logger.info("成功进入故事编辑页")
            return True
        log.logger.error("进入故事编辑页失败")
        return False

    def tap_album_droplist(self):
        """
            Summary:
                点击相册下拉列表
        """
        log.logger.info("点击最上方的下拉列表")
        self.album_drop_list_button.tap()
        time.sleep(3)
        log.logger.info("完成下拉列表的点击")

    def tap_in_diary_album(self):
        """
            Summary:
                点击in记相册
        """
        log.logger.info("点击in记相册")
        self.story_tab_in_diary_album_bar.tap()
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.text_to_be_present_in_element(
                    (MobileBy.ID, 'com.jiuyan.infashion:id/pic_text'), u'in记相册')
            )
            log.logger.info("成功展开in记相册")
            return True
        except TimeoutException:
            log.logger.error("展开in记相册失败")
            return False

    def select_photo_from_in_diary(self, index_list=[]):
        """
            Summary:
                从印记相册中选择照片上传
            Args:
                index_list: 照片序号列表
        """
        photo_list = self.in_diary_photo_list
        for index in index_list:
            log.logger.info("开始选择第{}张照片".format(index))
            photo_list[index-1].select()

        log.logger.info("照片已选择完毕")
        time.sleep(2)

    # *****************************公共方法********************************

    def tap_photo_tab(self):
        """
            Summary:
                点击图片tab
        :return:
        """
        log.logger.info("开始点击图片tab")
        self.photo_tab.tap()
        log.logger.info("点击完毕")
        time.sleep(2)
        return True

    def tap_story_tab(self):
        """
            Summary:
                点击故事tab页
        :return:
        """
        log.logger.info("开始点击故事tab")
        self.story_tab.tap()
        log.logger.info("点击完毕")
        try:
            WebDriverWait(self.base_parent, 10).until(
                EC.presence_of_element_located(
                    (MobileBy.ANDROID_UIAUTOMATOR,
                     'new UiSelector().className("android.widget.TextView").textContains("Hello!")')
                )
            )
            log.logger.info("故事集图片选择页已初始化完毕")
            return True
        except TimeoutException:
            log.logger.error("故事集图片选择未完成初始化")
            return False

    def is_continue_popup_exist(self):
        """
            Summary:
               判断继续遮罩是否存在
        Returns:

        """
        if self.wait_for_element_present(self.base_parent, timeout=3,
                                         id='com.jiuyan.infashion:id/tv_publish_menu_commen_msg_title'):
            log.logger.info("存在\"继续编辑上次临时保存的图片\"的提示遮罩")
            return True
        return False


class PostImgItem(base_frame_view.BaseFrameView):
    """
        Summary:
            上传的图片item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(PostImgItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    @property
    def check_box(self):
        """
            Summary:
                勾选框
        """
        id_ = 'com.jiuyan.infashion:id/item_photo_order'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def check_value(self):
        """
            Summary:
                选中显示的序号值
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/item_photo_order'
        return text_view.TextView(self._layout_view, id=id_).text

    def tap(self):
        """
            Summary:
                点击该图片
        :return:
        """
        log.logger.info("开始点击选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self._layout_view.click()
        time.sleep(1)
        log.logger.info("点击完毕")

    def select(self):
        """
            Summary:
                选择图片，点击图片区域即可选择，无需点击check_box
        """

        log.logger.info("开始点击选择{}图片".format('第'+str(self.__index+1)+'张' if self.__index is not None else '该'))
        self.check_box.tap()
        time.sleep(1)
        log.logger.info("完成选择, 已成功选中图片")

    def unselect(self):
        """
            Summary:
                取消选择图片
        """
        log.logger.info("开始取消选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self.check_box.tap()
        time.sleep(1)
        log.logger.info("完成取消, 已成功取消选择图片")

    def is_selected(self):
        """
            Summary:
                是否被选中
        :return:
        """
        if self.wait_for_element_present(timeout=5, id='com.jiuyan.infashion:id/item_photo_sel'):
            return True

        return False


class PostImgItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PostImgItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            return [PostImgItem(item.parent, item, index) for index, item in enumerate(self.__item_list)]
        return None

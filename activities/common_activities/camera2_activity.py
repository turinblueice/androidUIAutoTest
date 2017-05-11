#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: IN2.9版本拍照页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import image_button
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import text_view

from appium.webdriver import WebElement
from activities import activities
from selenium.common.exceptions import NoSuchElementException

import time


class Camera2Activity(base_frame_view.BaseFrameView):

    """
        Summary:
            拍照选择故事编辑页

        Attributes:

    """
    name = 'com.jiuyan.camera2.CameraActivity'
    
    def __init__(self, parent):
        super(Camera2Activity, self).__init__(parent)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = "com.jiuyan.infashion:id/camera_header_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def switch_camera_button(self):
        """
            Summary:
                切换摄像头按钮
        """
        id_ = "com.jiuyan.infashion:id/camera_header_switch_camera"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def menu_button(self):
        """
            Summary:
                菜单按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/camera_header_menu'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def camera(self):
        """
            Summary:
                相机按钮
        """
        id_ = 'com.jiuyan.infashion:id/live_bottom_take_btn'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def finish_camera_button(self):

        id_ = 'com.jiuyan.infashion:id/live_bottom_next'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def indicator_paster_button(self):
        """
            Summary:
                贴纸指示按钮
        Returns:

        """

        id_ = 'com.jiuyan.infashion:id/live_indicator_dpaster'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def paster_list(self):
        """
            Summary:
                贴纸列表
        Returns:

        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/camera_paster_list"]/' \
                 'android.widget.FrameLayout'
        return PasterItemList(self.base_parent, xpath=xpath_).item_list

    @property
    def indicator_filter_button(self):
        """
            Summary:
                滤镜按钮
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/live_indicator_filter'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def filter_list(self):
        """
            Summary:
                滤镜列表
        Returns:

        """
        xpath_ = '//android.support.v7.widget.RecyclerView[@resource-id="com.jiuyan.infashion:id/live_filter_recyclerview"]/' \
                 'android.widget.LinearLayout'
        return PasterItemList(self.base_parent, xpath=xpath_).item_list

    @property
    def photo_album_button(self):
        """
            Summary:
                进入照片集按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/live_bottom_album_cover'
        return image_view.ImageView(self.parent, id=id_)

    # ************************操作***************************
    def tap_camera(self):
        """
            Summary:
                点击摄像头
        """
        time.sleep(2)
        log.logger.info("点击摄像头")
        self.camera.tap()
        log.logger.info("摄像头已点击")

        # 等待下一步按钮出现
        if self.wait_for_element_present(self.parent, timeout=4, id='com.jiuyan.infashion:id/live_bottom_next'):
            log.logger.info("拍照已完成")
            return True
        log.logger.error("拍照错误")
        return False

    def tap_finish_camera(self):
        """
            Summary:
                点击拍照完成按钮
        """
        log.logger.info("点击完成拍照按钮")
        self.finish_camera_button.tap()
        log.logger.info("完成拍照按钮已点击")
        if self.wait_activity(activities.ActivityNames.PUBLISH_CORE, 10):
            log.logger.info("成功进入拍照加工页")
            return True
        log.logger.error("进入拍照加工页面失败")
        return False

    def tap_album_button(self, timeout=10):
        """
            Summary:
                点击进入照片集合按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击进入照片集合按钮")

        self.photo_album_button.tap()
        if self.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, timeout):
            log.logger.info("成功进入照片集合按钮")
            return True
        else:
            log.logger.error("进入照片集合按钮失败")
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


class PasterItem(base_frame_view.BaseFrameView):
    """
        Summary:
            贴纸item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(PasterItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    def is_selected(self):

        if self.wait_for_element_present(timeout=3, id='com.jiuyan.infashion:id/iv_paster_border'):
            log.logger.info("第{}个贴纸已被选中".format(self.__index))
            return True
        log.logger.error("第{}个贴纸未选中".format(self.__index))
        return False

    def tap(self):
        """
            Summary:
                点击该图片
        """
        log.logger.info("开始点击选择{}照片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self._layout_view.click()
        time.sleep(2)
        log.logger.info("点击完毕")

    def select(self):
        """
            Summary:
                选择图片，点击图片区域即可选择，无需点击check_box
        """

        log.logger.info("开始点击选择{}贴纸".format('第'+str(self.__index)+'张' if self.__index is not None else '该'))
        self._layout_view.click()
        if self.wait_for_element_present(timeout=3, id='com.jiuyan.infashion:id/iv_paster_border'):
            log.logger.info("第{}个贴纸已被选中".format(self.__index))
            return True
        log.logger.error("第{}个贴纸未选中".format(self.__index))
        return False


class PasterItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PasterItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            return [PasterItem(item.parent, item, index) for index, item in enumerate(self.__item_list, start=1)]
        return None


class FilterItem(base_frame_view.BaseFrameView):
    """
        Summary:
            滤镜item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(FilterItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    @property
    def name(self):

        return text_view.TextView(self._layout_view, id='com.jiuyan.infashion:id/live_item_filter_name').text

    def tap(self):
        """
            Summary:
                点击该图片
        """
        log.logger.info("开始点击选择{}照片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self._layout_view.click()
        time.sleep(2)
        log.logger.info("点击完毕")

    def select(self):
        """
            Summary:
                选择图片，点击图片区域即可选择，无需点击check_box
        """
        name_ = self.name
        log.logger.info("开始点击选择滤镜\"{}\"".format(name_))
        self._layout_view.click()
        log.logger.info("点击完毕")
        time.sleep(3)


class FilterItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(FilterItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            return [FilterItem(item.parent, item, index) for index, item in enumerate(self.__item_list, start=1)]
        return None

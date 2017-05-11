#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 拍照故事编辑页

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log

from gui_widgets.basic_widgets import image_button
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import text_view

from appium.webdriver import WebElement
from activities import activities
from selenium.common.exceptions import NoSuchElementException

import time


class StoryCameraActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            拍照编辑页

        Attributes:

    """
    name = 'com.jiuyan.camera.activity.StoryCameraActivity'
    
    def __init__(self, parent):
        super(StoryCameraActivity, self).__init__(parent)

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = "com.jiuyan.infashion:id/btn_header_back"
        return image_button.ImageButton(self.parent, id=id_)

    @property
    def switch_camera_button(self):
        """
            Summary:
                切换摄像头按钮
        """
        id_ = "com.jiuyan.infashion:id/btn_header_switch"
        return image_button.ImageButton(self.parent, id=id_)

    @property
    def photo_bar_hide_display_button(self):
        """
            Summary:
                照片栏隐藏/显示按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/camera_photo_bar_hide_btn'
        return image_view.ImageView(self.parent, id=id_)

    @property
    def camera(self):
        """
            Summary:
                相机按钮
        """
        id_ = 'com.jiuyan.infashion:id/camera_capture'
        return button.Button(self.parent, id=id_)

    @property
    def photo_list(self):
        """
            Summary:
                已存在图片列表
        """
        id_ = 'com.jiuyan.infashion:id/item_photo_root'
        return PhotoItemList(self.parent, id=id_).item_list

    @property
    def next_step_button(self):
        """
            Summary:
                下一步按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/camera_bottom_next_step'
        return text_view.TextView(self.parent, id=id_)

    # ************************操作***************************
    def tap_camera(self):
        """
            Summary:
                点击摄像头
        """
        log.logger.info("点击摄像头")
        self.camera.tap()
        time.sleep(4)
        log.logger.info("摄像头已点击")

    def select_photos(self, *indexes):
        """
            Summary:
                选择图片
            Args:
                *indexes: 图片序号元组
        """
        for index in indexes:
            log.logger.info("开始选择第{}张图片".format(index))
            self.photo_list[index-1].tap()
            log.logger.info("选择完毕")
            time.sleep(2)

    def tap_next_step_button(self, timeout=10):
        """
            Summary:
                点击下一步按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击下一步按钮")
        self.next_step_button.tap()
        if self.wait_activity(activities.ActivityNames.PUBLISH_CORE, timeout):
            log.logger.info("成功进入图片发布加工页")
            return True
        else:
            log.logger.error("进入图片发布页加工失败")
            return False


class PhotoItem(base_frame_view.BaseFrameView):
    """
        Summary:
            照片item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(PhotoItem, self).__init__(parent)
        self._layout_view = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__is_select = False
        self.__index = index

    def __getattr__(self, item):
        return getattr(self._layout_view, item, None)

    @property
    def selected_value(self):
        """
            Summary:
                选中序号
        """
        id_ = 'com.jiuyan.infashion:id/item_photo_order'
        return text_view.TextView(self._layout_view, id=id_).text

    @property
    def is_selected(self):

        try:
            text_view.TextView(self._layout_view, id='com.jiuyan.infashion:id/item_photo_order')
            return True
        except NoSuchElementException:
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
        if not self.__is_select:
            log.logger.info("开始点击选择{}图片".format('第'+str(self.__index)+'张' if self.__index is not None else '该'))
            self._layout_view.click()
            if self.wait_for_element_present(5, 1, id='com.jiuyan.infashion:id/item_photo_order'):
                log.logger.info("选中标记出现，已选中")
                self.__is_select = True
                log.logger.info("完成选择")
                log.logger.info("已成功选中图片")
                return True
            log.logger.error("选中图片失败")
            return False

    def unselect(self):
        """
            Summary:
                取消选择图片
        """
        if self.__is_select:
            log.logger.info("开始取消选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
            self._layout_view_item.click()
            if not self.wait_for_element_present(5, 1, id='com.jiuyan.infashion:id/item_photo_order'):
                log.logger.info("选中标记已消失，已取消选择")
                self.__is_select = False
                log.logger.info("完成取消")
                return True
            log.logger.error("取消选中失败")
            return False


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

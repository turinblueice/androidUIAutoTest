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

from appium.webdriver import WebElement
from activities import activities

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


class PhotoPickerActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            选择图片页面

        Attributes:

    """
    name = '.lib.component.photopicker.core.PhotoPickerActivity'
    
    def __init__(self, parent):
        super(PhotoPickerActivity, self).__init__(parent)
        self.__frame_view = frame_layout.FrameLayout(self.parent, id='android:id/content')

    @property
    def back_button(self):
        """
            Summary:
                返回按钮
        """
        id_ = "com.jiuyan.infashion:id/btnback"
        return button.Button(self.__frame_view, id=id_)

    @property
    def next_step_button(self):
        """
            Summary:
                下一步按钮
        """
        id_ = "com.jiuyan.infashion:id/btnright"
        return button.Button(self.__frame_view, id=id_)

    @property
    def camera(self):
        """
            Summary:
                相机按钮
        """
        xpath_ = '//android.widget.GridView[@resource-id="com.jiuyan.infashion:id/id_gridView"]/' \
                 'android.widget.FrameLayout[1]'
        return frame_layout.FrameLayout(self.base_parent, xpath=xpath_)

    @property
    def post_image_list(self):
        """
            Summary:
                要上传的图片列表
        """
        xpath_ = '//android.widget.GridView[@resource-id="com.jiuyan.infashion:id/id_gridView"]/' \
                 'android.widget.FrameLayout'

        # 只有webdriver对象支持xpath查询，webelement对象不支持
        return PostImgItemList(self.base_parent, xpath=xpath_).item_list[1:]

    # ************************操作***************************
    def open_camera(self):
        """
            Summary:
                打开摄像头
        """
        log.logger.info("点击打开摄像头")
        self.camera.tap()
        time.sleep(2)
        log.logger.info("摄像头已打开")

    def select_image(self, index):
        """
            Summary:
                选择要上传的图片
            Args:
                index: 图片序号
        """
        self.post_image_list[index-1].select()
        time.sleep(1)

    def unselect_image(self, index):
        """
            Summary:
                取消选择上传的图片
            Args:
                index: 图片序号
        """
        self.post_image_list[index-1].unselect()
        time.sleep(1)

    def tap_next_step_button(self, timeout=10):
        """
            Summary:
                点击下一步按钮
            Args:
                timeout:等待时长
        """
        log.logger.info("开始点击下一步按钮")
        self.next_step_button.tap()
        try:
            WebDriverWait(self.base_parent, timeout).until(
                lambda d: d.current_activity.lower().find('crop') > -1)
            return True
        except TimeoutException:
            return False


class PostImgItem(base_frame_view.BaseFrameView):
    """
        Summary:
            上传的图片item
    """
    def __init__(self, parent, item=None, index=None, **kwargs):
        super(PostImgItem, self).__init__(parent)
        self.__post_img_item = item if isinstance(item, WebElement) else self.find_element(**kwargs)
        self.__is_select = False
        self.__index = index

    def __getattr__(self, item):
        return getattr(self.__post_img_item, item, None)

    @property
    def check_box(self):
        """
            Summary:
                勾选框
        """
        id_ = 'com.jiuyan.infashion:id/id_item_select'
        return image_button.ImageButton(self.__post_img_item, id=id_)

    def tap(self):
        """
            Summary:
                点击该图片
        :return:
        """
        log.logger.info("开始点击选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
        self.__post_img_item.click()
        time.sleep(2)
        log.logger.info("点击完毕")

    def select(self):
        """
            Summary:
                选择图片，点击图片区域即可选择，无需点击check_box
        """
        if not self.__is_select:
            log.logger.info("开始点击选择{}图片".format('第'+str(self.__index)+'张' if self.__index is not None else '该'))
            self.__post_img_item.click()
            time.sleep(1)
            self.__is_select = True
            log.logger.info("完成选择")
        log.logger.info("已成功选中图片")

    def unselect(self):
        """
            Summary:
                取消选择图片
        """
        if self.__is_select:
            log.logger.info("开始取消选择{}图片".format('第' + str(self.__index) + '张' if self.__index is not None else '该'))
            self.__post_img_item.click()
            time.sleep(1)
            self.__is_select = False
            log.logger.info("完成取消")
        log.logger.info("已成功取消选择图片")


class PostImgItemList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(PostImgItemList, self).__init__(parent)
        self.__item_list = self.find_elements(**kwargs)

    @property
    def item_list(self):
        if self.__item_list:
            log.logger.info("可视区域内图片个数为{}".format(len(self.__item_list)))
            return [PostImgItem(item.parent, item, index) for index, item in enumerate(self.__item_list, start=0)]
        return None

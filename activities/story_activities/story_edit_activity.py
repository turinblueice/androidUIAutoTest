#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 用户中心-编辑资料

Authors: Turinblueice
Date: 2016/7/27
"""
from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import image_view
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import edit_text
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import button
from gui_widgets.basic_widgets import frame_layout
from gui_widgets.basic_widgets import scroll_view
from gui_widgets.basic_widgets import recycler_view
from gui_widgets.custom_widgets import alert

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from activities import activities

import time
import random


class StoryEditActivity(base_frame_view.BaseFrameView):

    """
        Summary:
            发布故事集-编辑故事页

        Attributes:

    """
    name = '.story.StoryEditActivity'  # 用户设置页的activity名称

    def __init__(self, parent):
        super(StoryEditActivity, self).__init__(parent)
        self.__root_view = relative_layout.RelativeLayout(self.parent, id='com.jiuyan.infashion:id/story_edit_act_root')

        # 滑动区域，覆盖父类的属性
        self._scroll_view = linear_layout.LinearLayout(self.parent, id='com.jiuyan.infashion:id/rv_story_edit')

    @property
    def title(self):
        """
            Summary:
                标题-编辑故事
        """
        id_ = "com.jiuyan.infashion:id/tv_story_edit_title"
        return text_view.TextView(self.parent, id=id_).text

    @property
    def back_button(self):
        """
            Summary:
                后退按钮
        """
        id_ = "com.jiuyan.infashion:id/iv_story_edit_back"
        return image_view.ImageView(self.parent, id=id_)

    @property
    def preview_button(self):
        """
            Summary:
                预览按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/tv_story_edit_confirm'
        return text_view.TextView(self.parent, id=id_)

    @property
    def add_diary_page_button(self):
        """
            Summary:
                页面最下方的故事段落添加按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_add_item'
        return text_view.TextView(self.parent, id=id_)

    @property
    def add_diary_page_button_middle(self):
        """
            Summary：
                故事页中间的添加按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_add_view'
        return linear_layout.LinearLayout(self.parent, id=id_)

    @property
    def diary_cover_detail(self):

        return DiaryCover(self.__root_view)

    @property
    def diary_page_list(self):

        return DiaryPageDetailList(self.__root_view, id='com.jiuyan.infashion:id/left_drag_view').page_list

    # ************************操作***************************

    def tap_preview_button(self):
        """
            Summary:
                点击预览按钮
        :return:
        """
        log.logger.info("开始点击预览按钮")
        self.preview_button.tap()
        log.logger.info("点击完毕")
        if self.wait_activity(activities.ActivityNames.STORY_DETAIL, 10):
            log.logger.info("成功进入故事预览页")
            return True
        log.logger.error("进入预览页失败")
        return False


class DiaryCover(base_frame_view.BaseFrameView):
    """
        Summary:
            日记故事封面/开头模块
    """
    def __init__(self, parent):
        super(DiaryCover, self).__init__(parent)
        self._layout_view = recycler_view.RecyclerView(
            self.parent, id='com.jiuyan.infashion:id/diary_id_timeline_recyclerview')

    @property
    def diary_name_edit_box(self):
        """
            Summary:
                故事名称编辑框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/et_story_cover_name'
        return edit_text.EditText(self._layout_view, id=id_)

    @property
    def diary_cover_date(self):
        """
            Summary:
                故事时间
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/et_story_cover_date'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def diary_cover_location(self):
        """
            Summary:
                故事地点
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/et_story_cover_location'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def diary_beginning_edit_box(self):
        """
            Summary:
                故事开头编辑框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_story_edit_beginning'
        return edit_text.EditText(self._layout_view, id=id_)

    @property
    def diary_cover(self):
        """
            Summary:
                封面
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/iv_story_cover_bg'
        return image_view.ImageView(self._layout_view, id=id_)

    @property
    def popup_cover_list(self):
        """
            Summary:
                弹出框封面图片列表
        :return:
        """
        recycler_view_ = recycler_view.RecyclerView(self.base_parent, id='com.jiuyan.infashion:id/rv_cover_list')
        return relative_layout.RelativeLayoutList(
            recycler_view_, id='com.jiuyan.infashion:id/item_photo_root').relative_layout_list

    # **************************操作方法********************************

    def input_diary_name(self, *values):
        """
            Summary:
                输入故事名称
        """
        log.logger.info("开始输入故事名称")
        self.diary_name_edit_box.clear_text_field()
        self.diary_name_edit_box.send_keys(*values)
        time.sleep(1)
        log.logger.info("故事名称输入完毕")

    def input_diary_beginning(self, *values):
        """
            Summary:
                添加故事开头
            Args:
                values: 元组，编辑的值
        """
        log.logger.info("开始添加故事的开头")
        self.diary_beginning_edit_box.clear_text_field()
        self.diary_beginning_edit_box.send_keys(*values)
        time.sleep(1)
        log.logger.info("故事开头完成输入")

    def tap_cover_for_setting(self):
        """
            Summary:
                点击图片设置封面
        :return:
        """
        log.logger.info("点击图片封面")
        self.diary_cover.tap()
        log.logger.info("完成封面点击")
        try:
            WebDriverWait(self.base_parent, 10).until(
                (MobileBy.ID, 'com.jiuyan.infashion:id/rv_cover_list')
            )
            log.logger.info("成功吊起封面面板")
            return True
        except:
            log.logger.error("吊起封面面板失败")
            return False

    def select_cover(self, index):
        """
            Summary:
                选择封面图片
            Args:
                index：序号
        """
        log.logger.info("点击第{}张图片".format(index))
        curr_cover = self.popup_cover_list[index-1]
        curr_cover.tap()
        log.logger.info("点击完毕")
        log.logger.info("开始检测该图片是否被选中")

        if self.wait_for_element_present(parent=curr_cover, id='com.jiuyan.infashion:id/selected_cover'):
            log.logger.info("该图片已选中")
            return True
        log.logger.error("该图片未选中")
        return False


class DiaryPageDetail(base_frame_view.BaseFrameView):
    """
        Summary:
            故事集每一页
    """
    def __init__(self, parent, page_item=None, **kwargs):
        super(DiaryPageDetail, self).__init__(parent)
        if kwargs:
            self._layout_view = page_item if isinstance(relative_layout, WebElement) else self.find_element(**kwargs)
        else:
            self._layout_view = page_item if isinstance(relative_layout, WebElement) else self.find_element(
                id='com.jiuyan.infashion:id/left_drag_view'
            )

    @property
    def photo(self):
        """
            Summary:
                照片面板
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_image_layout'
        return frame_layout.FrameLayout(self._layout_view, id=id_)

    @property
    def diary_page_description_edit_box(self):
        """
            Summary:
                故事描述编辑框
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_description'
        return edit_text.EditText(self._layout_view, id=id_)

    @property
    def diary_page_description_time(self):
        """
            Summary:
                故事描述的时间
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_time'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def diary_page_description_location(self):
        """
            Summary:
                故事地点
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_location'
        return text_view.TextView(self._layout_view, id=id_)

    @property
    def edit_right_menu(self):
        """
            Summary:
                右侧边栏编辑组图按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_right_menu'
        return relative_layout.RelativeLayout(self._layout_view, id=id_)

    @property
    def add_diary_photo_button(self):
        """
            Summary:
                侧边栏故事图片添加按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_add'
        return frame_layout.FrameLayout(self._layout_view, id=id_)

    @property
    def delete_diary_page_button(self):
        """
            Summary:
                侧边栏删除故事按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_rm'
        return frame_layout.FrameLayout(self._layout_view, id=id_)

    @property
    def move_down_button(self):
        """
            Summary:
                下移按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_down_btn'
        return frame_layout.FrameLayout(self._layout_view, id=id_)

    @property
    def move_up_button(self):
        """
            Summary:
                上移按钮
        """
        id_ = 'com.jiuyan.infashion:id/story_edit_item_up_btn'
        return frame_layout.FrameLayout(self._layout_view, id=id_)

    @property
    def magic_button(self):
        """
            Summary:
                呼出的编辑菜单的魔法棒加工按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/btn_filter'
        return image_view.ImageView(self.base_parent, id=id_)

    @property
    def change_button(self):
        """
            Summary:
                呼出编辑菜单的更换按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/btn_change'
        return image_view.ImageView(self.base_parent, id=id_)

    @property
    def delete_button(self):
        """
            Summary:
                呼出编辑菜单的删除按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/btn_del'
        return image_view.ImageView(self.base_parent, id=id_)

    @property
    def zoom_in_button(self):
        """
            Summary:
                呼出编辑菜单的放大按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/btn_zoom_in'
        return image_view.ImageView(self.base_parent, id=id_)

    @property
    def zoom_out_button(self):
        """
            Summary:
                呼出编辑菜单的缩小按钮
        :return:
        """
        id_ = 'com.jiuyan.infashion:id/zoom_out'
        return image_view.ImageView(self.base_parent, id=id_)

    # ************************操作方法******************************

    def input_diary_description(self, *values):
        """
            Summary:
                输入故事描述
        """
        log.logger.info("开始输入故事描述")
        self.diary_page_description_edit_box.clear_text_field()
        self.diary_page_description_edit_box.send_keys(*values)
        time.sleep(1)
        log.logger.info("故事描述输入完毕")

    def tap_right_menu(self):
        """
            Summary:
                点击侧边栏菜单
        """
        log.logger.info("点击侧边栏编辑组图菜单")
        self.edit_right_menu.tap()
        time.sleep(2)
        log.logger.info("完成编辑组图菜单点击")

    def tap_add_photo_button(self):
        """
            Summary:
                点击增加照片按钮
        :return:
        """
        log.logger.info("点击增加照片按钮")
        self.add_diary_photo_button.tap()
        log.logger.info("完成点击")
        if self.wait_activity(activities.ActivityNames.PHOTO_STORY_GALLERY, 10):
            log.logger.info("成功进入图片选择页")
            return True
        log.logger.error("进入图片选择页失败")
        return False

    def tap_delete_story_item_button(self, accept=True):
        """
            Summary:
                点击删除故事描述/图片按钮
            Args:
                accept:True:点击确认对话框的确定按钮；False:点击确认对话框的取消按钮
        :return:
        """
        log.logger.info("点击删除故事按钮")
        self.delete_diary_page_button.tap()
        log.logger.info("完成删除按钮点击")

        #  等待对话框弹出
        if self.wait_for_element_present(self.base_parent, id='com.jiuyan.infashion:id/parentPanel'):
            log.logger.info("弹出确认对话框")
            curr_alert = alert.Alert()
            if accept:
                curr_alert.confirm_button.tap()
            else:
                curr_alert.cancel_button.tap()
            return True
        log.logger.error("确认对话框未弹出")
        return False

    def tap_photo_to_display_menu(self):
        """
            Summary:
                点击照片唤起操作菜单
        :return:
        """
        log.logger.info("开始点击照片按钮")
        self.photo.tap()
        log.logger.info("点击完毕")
        if self.wait_for_element_present(parent=self.base_parent, id='com.jiuyan.infashion:id/btn_filter'):
            log.logger.info("编辑菜单已呼出")
            return True
        log.logger.error("没有呼出编辑菜单")
        return False


class DiaryPageDetailList(base_frame_view.BaseFrameView):

    def __init__(self, parent, **kwargs):
        super(DiaryPageDetailList, self).__init__(parent)
        self.__layout_view_list = self.find_elements(**kwargs)

    @property
    def page_list(self):
        if self._layout_view:
            return [DiaryPageDetail(item.parent, item) for item in self.__layout_view_list]
        return None


#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为底部玩字弹层
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from util import log
from gui_widgets.basic_widgets import linear_layout
from gui_widgets.basic_widgets import text_view
from gui_widgets.basic_widgets import edit_text

from activities import activities

import time


class BottomPopupArtTextWindow(base_frame_view.BaseFrameView):
    """
        Summary:
            底部的弹层
    """

    popup_id = 'com.jiuyan.infashion:id/publish_art_text_inputview'

    def __init__(self, parent, **kwargs):
        super(BottomPopupArtTextWindow, self).__init__(parent)
        if kwargs:
            self._linear_layout = linear_layout.LinearLayout(self.parent, **kwargs)
        else:
            self._linear_layout = linear_layout.LinearLayout(self.parent, id=self.popup_id)
        self.__words = None

    def __getattr__(self, item):

        if hasattr(self._linear_layout, item):
            return getattr(self._linear_layout, item)
        return getattr(self.base_parent, item)

    @property
    def edit_box(self):
        """
            Summary:
                临时保存按钮
        """
        id_ = 'com.jiuyan.infashion:id/et_content'
        return edit_text.EditText(self._linear_layout, id=id_)

    @property
    def words_limit(self):
        """
            Summary:
                文字限制
        Returns:

        """
        id_ = 'com.jiuyan.infashion:id/tv_text_limit'
        return text_view.TextView(self._linear_layout, id=id_).text

    @property
    def use_button(self):
        """
            Summary:
                使用按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_send'
        return text_view.TextView(self._linear_layout, id=id_)

    @property
    def change_button(self):
        """
            Summary:
                换一换按钮
        """
        id_ = 'com.jiuyan.infashion:id/tv_business_change_wordart'
        return text_view.TextView(self._linear_layout, id=id_)

    @property
    def words_available_list(self):
        """
            Summary:
                推荐的词语列表
        Returns:

        """
        xpath_ = '//android.widget.RelativeLayout[@resource-id=\"com.jiuyan.infashion:id/v_business_word_art_group\"]/' \
                 'android.widget.TextView'
        return text_view.TextViewList(self.base_parent, xpath=xpath_).text_view_list

    # *************************操作方法**********************

    def tap_use_button(self):
        """
            Summary:
                点击使用按钮
        """
        log.logger.info("开始点击使用按钮")
        self.use_button.tap()
        log.logger.info("完成临时保存按钮的点击")
        if self.wait_for_element_disappear(self.base_parent, timeout=5, id='com.jiuyan.infashion:id/publish_art_text_inputview'):
            log.logger.info("玩字遮罩已取消")
            return True
        log.logger.error("玩字遮罩还存在")
        return False

    def tap_change_button(self):
        """
            Summary:
                点击换一换按钮
        """
        log.logger.info("开始点击换一换按钮")
        self.change_button.tap()
        log.logger.info("完成换一换按钮的点击")
        time.sleep(3)

    def input_words(self, value):

        self.__words = value
        log.logger.info("开始输入文字")
        self.edit_box.clear_text_field()
        self.edit_box.send_keys(value)
        log.logger.info("完成文字输入")
        time.sleep(2)

    def select_words_available(self, index=0):
        """
            Summary:

        Returns:

        """
        log.logger.info("选择第{}个词组".format(index+1))
        words = self.words_available_list[index]
        words.tap()
        self.__words = unicode(words.text, 'utf8')
        log.logger.info("\"{}\"选择完毕".format(words.text))
        time.sleep(2)

    def words_length_check(self):
        """
            Summary:
                检查文字长度
        Returns:

        """
        expected_length = int(self.words_limit.split('/')[0])
        actual_length = len(self.__words)

        return expected_length == actual_length
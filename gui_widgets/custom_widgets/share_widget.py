#-*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明:该模块为分享组件的分装
 
Authors: Turinblueice
Date:    16/3/16 16:46
"""

from base import base_frame_view
from gui_widgets.basic_widgets import grid_view
from gui_widgets.basic_widgets import relative_layout
from gui_widgets.basic_widgets import text_view
from util import log


class ShareWidgets(base_frame_view.BaseFrameView):

    TO_CLIENTS = "发送给客户"
    TO_WECHAT = "微信"
    TO_MOMENTS = "朋友圈"
    TO_QQ = "QQ"
    TO_QQ_SPACE = "QQ空间"
    TO_COPY_LINK = "复制链接"
    TO_WEIBO = "新浪微博"
    TO_MESSAGE = "短信"
    TO_TWO_DIMENSION = "二维码"

    send_to_clients_activity = '.business.share.ui.SendToUserListActivity'

    def __init__(self, parent):
        super(ShareWidgets, self).__init__(parent)
        self.__id = 'com.qima.kdt:id/content_layout'
        self.__content_view = relative_layout.RelativeLayout(self._parent, id=self.__id)
        self.__grid_view = grid_view.GridView(self.__content_view, id='com.qima.kdt:id/grid_view')
        self.__grid_text_view_list = text_view.TextViewList(
            self.__grid_view, type='android.widget.TextView').text_view_list

    @property
    def cancel_button(self):
        """
            Summary:
                取消按钮
        """
        id_ = 'com.qima.kdt:id/btn_cancel'
        return text_view.TextView(self.__content_view, id=id_)

    def get_list_item(self, index):
        """
        获取Grid中的item

        Args:
            index: 列表中元素的序号
        """
        return self.__grid_text_view_list[index]

    @property
    def to_clients(self):
        """
        发送给客户

        Return:
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_CLIENTS))

    @property
    def to_wechat(self):
        """
        微信

        Return:
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_WECHAT))

    @property
    def to_moments(self):
        """
        朋友圈

        Return:
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_MOMENTS))

    @property
    def to_qq(self):
        """
        qq

        Return:
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_QQ))

    @property
    def to_qq_space(self):
        """
            QQ 空间
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_QQ_SPACE))

    @property
    def to_copy_link(self):
        """
            复制链接
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_COPY_LINK))

    @property
    def to_weibo(self):
        """
            新浪微博
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_WEIBO))

    @property
    def to_message(self):
        """
            短信
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(self.TO_MESSAGE))

    @property
    def to_two_dimension_code(self):
        """
            二维码
        """
        return text_view.TextView(self.__grid_view, uiautomator='new UiSelector().text("{}")'.format(
            self.TO_TWO_DIMENSION))

    def cancel_share(self):
        """
            Summary:
                取消分享
        """

        self.cancel_button.tap()

    def share_to_clients(self):
        """
            Summary:
                分享给客户
        """
        log.logger.info("点击分享给客户")
        self.to_clients.tap()
        if self.base_parent.wait_activity(self.send_to_clients_activity, 10):
            log.logger.info("进入接待客户列表页")
        else:
            log.logger.info("进入接待客户列表页失败")

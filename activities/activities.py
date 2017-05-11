#  -*-coding:utf8-*-

################################################################################
#
#
#
################################################################################
"""
模块用法说明: 应用各activity的名称

Authors: Turinblueice
Date: 2016/7/28
"""


class ActivityNames(object):

    LOGIN_MAIN = '.login.MainActivity'   # 登录页的名称
    IN_MAIN = '.InHomeActivity'  # in主页名称
    LOGIN_FRIEND_RECOMMEND = '.login.activity.FriendRecommendActivity'  # 登录的好友推荐页
    LOGIN_GUIDE_CAMERA = '.login.activity.GuideCameraActivity'  # 登录引导页
    LOGIN_GUIDE_VIDEO = '.login.activity.VideoGuideActivity'  # 登录视频引导页

    USER_INFO = '.usercenter.activity.EditInfoActivity'  # 编辑资料activity名称
    CROPPER = '.lib.component.cropper.CropperActivity'  # 裁剪图片activity名称
    USER_SETTING = '.usercenter.activity.setting.UserCenterSettingActivity'  # 用户设置页的activity名称

    PHOTO_PICKER = '.lib.component.photopicker.core.PhotoPickerActivity'  # 照片上传activity名称
    PASTER_MALL = '.module.paster.activity.PasterMallActivity'  # 我的贴纸activity名称
    CUSTOM_PASTER_CROP = '.module.paster.custom.activities.CustomPasterCropActivity'   # 自定义贴纸裁剪activity名称
    CUSTOM_PASTER_EDITOR = '.module.paster.custom.activities.CustomPasterEditorActivity'  # 自定义贴纸搭配页
    SELECT_PHOTO_GUIDE = '.module.paster.custom.activities.SelectPhotoGuideActivity'  # 图片选择引导页
    CUT_OUT_PASTER = '.module.paster.custom.activities.CutOutActivity'  # 图片编辑筛选页

    STORY_CAMERA = 'com.jiuyan.camera.activity.StoryCameraActivity'  # 拍照故事编辑页
    CAMERA2 = 'com.jiuyan.camera2.CameraActivity'  # 拍照页面IN2.9.9
    PUBLISH_CORE = '.publish.PublishCoreActivity'  # 图片加工发布页面
    PUBLISH = '.publish.component.publish.activity.PublishActivity'  # 图片发布页

    PHOTO_STORY_GALLERY = '.album.StoryGalleryActivity'  # 故事集/图片选择页

    STORY_EDIT = '.story.StoryEditActivity'  # 故事编辑页
    STORY_DETAIL = '.story.activity.StoryDetailsAct'  # 故事集预览/详情页
    STORY_SETTING = '.story.activity.StorySettingActivity'  # 故事集设置页
    STORY_SHARE = '.story.activity.StoryShareActivity2'  # 故事发布成功分享页

    ADD_FRIEND = '.usercenter.activity.UserCenterFriendsAddActivity'  # 添加好友页
    USER_CENTER_FRIEND = '.usercenter.activity.UserCenterFriendsActivity'  # 用户中心的我的好友页

    DIARY_INFO = '.diary.other.v260.DiaryOtherActivity'  # 好友in记页
    PHOTO_ALBUM_CORE = '.photo.PhotoCoreActivity'  # 图片集详情页

    TOPIC_DETAIL = '.module.tag.activity.TagActivityV253'  # 话题详情页
    TOPIC_SQUARE = '.module.square.men.activity.SquareMenTopicActivity'  # 热门话题广场页
    FRIEND_PHOTO_DETAIL = '.friend.activity.FriendPhotoDetailActivity'  # 好友图片详情页
    FRIEND_PHOTO_RECOMMEND_DETAIL = '.friend.activity.FriendPhotoDetailRecommendActivity'  # 好友图片详情页
    FRIEND_PHOTO_VIEW = '.friend.activity.FriendPhotoViewPagerActivity'  # 单图页
    PHOTO_PRIVACY = '.friend.activity.FriendPhotoPrivacyActivity'  # 图片详情页权限更改

    FOLLOWED_FANS_LIST = '.diary.follower.FollowedListActivity'  # fans列表

    PUBLISH_TAG = '.publish.component.tag.PublishTagActivity'  # 发布标签页
    PUBLISH_WORDS = '.publish.component.wordartformen.activity.PublishWordArtForMenActivity'  # 玩字页面

    LIVE = 'com.jiuyan.livecam.activities.AudienceWatchLiveAct'  # 直播页面
    WEBVIEW = '.lib.webview.BrowserForNativeAvtivity'  # WebView页面

    SQUARE_CATEGORY = '.module.square.activity.SquareCategoryActivity'  # 话题广场分类页面

    TALENT_RECOMMEND = '.module.square.activity.EretarActivity'  # 达人分类推荐
    ESSENCE_RECOMMEND = '.module.square.activity.EssenceRecActivity'  # 精选推荐
    REMARK = '.usercenter.activity.UserCenterReMarkActicity'  # 个人in记中心,更改他人资料页面
    BIG_HEAD = '.diary.other.v260.DiaryBigHeadAct'  # 头像详情

    QQ_AUTH = 'com.tencent.open.agent.AuthorityActivity'  # QQ登录授权页
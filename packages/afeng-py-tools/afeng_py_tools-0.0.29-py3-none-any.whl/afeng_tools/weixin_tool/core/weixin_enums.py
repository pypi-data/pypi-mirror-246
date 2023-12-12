import os
from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel

from afeng_tools.os_tool.os_tools import get_user_home
from afeng_tools.weixin_tool.core.model.item.wx_receive_event_models import WeixinEventItem, WeixinSubscribeEventItem, \
    WeixinQrEventItem, WeixinScanEventItem, WeixinLocationEventItem, WeixinMenuEventItem
from afeng_tools.weixin_tool.core.model.item.wx_receive_msg_models import WeixinVoiceMsgItem, WeixinTextMsgItem, \
    WeixinImageMsgItem, WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from afeng_tools.weixin_tool.core.response import XmlResponse


class WeixinConfigItem(BaseModel):
    """微信配置枚举"""
    weixin_app_id: str
    weixin_app_secret: str
    weixin_token: str
    weixin_encoding_aes_key: str
    weixin_msg_callback: Callable[[
        WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem | WeixinSubscribeEventItem | WeixinQrEventItem | WeixinScanEventItem | WeixinLocationEventItem | WeixinMenuEventItem], XmlResponse]
    weixin_token_file: Optional[str] = os.path.join(get_user_home(), f'.wx_access_token.bin')


class WeixinConfigKeyEnum(Enum):
    """微信配置枚举"""
    # 微信公众号app_id
    weixin_app_id = 'weixin_app_id'
    # 微信公众号app_secret
    weixin_app_secret = 'weixin_app_secret'
    # 微信公众号token
    weixin_token = 'weixin_token'
    # 微信公众号token
    weixin_encoding_aes_key = 'weixin_encoding_aes_key'
    # 微信公众号接到消息后的回调函数
    weixin_msg_callback = 'weixin_msg_callback'
    # 微信公众号token文件的存储路径
    weixin_token_file = 'weixin_token_file'
    # 小程序 appId
    mp_app_id = 'mp_app_id'
    # 小程序 appSecret
    mp_app_secret = 'mp_app_secret'

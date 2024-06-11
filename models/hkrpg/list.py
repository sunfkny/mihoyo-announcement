from __future__ import annotations

import datetime
from typing import List

from pydantic import BaseModel


class ListItem1(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    type_label: str
    tag_label: str
    tag_icon: str
    login_alert: int
    lang: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    type: int
    remind: int
    alert: int
    tag_start_time: str
    tag_end_time: str
    remind_ver: int
    has_content: bool
    extra_remind: int
    tag_icon_hover: str


class ListItem(BaseModel):
    list: List[ListItem1]
    type_id: int
    type_label: str


class TypeListItem(BaseModel):
    id: int
    name: str
    mi18n_name: str


class ListItem2(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    type_label: str
    tag_label: str
    tag_icon: str
    login_alert: int
    lang: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    type: int
    remind: int
    alert: int
    tag_start_time: str
    tag_end_time: str
    remind_ver: int
    has_content: bool
    pic_type: int
    content_type: int
    img: str
    href_type: int
    href: str
    pic_list: List
    extra_remind: int


class TypeListItem1(BaseModel):
    list: List[ListItem2]
    pic_type: int


class PicListItem(BaseModel):
    type_list: List[TypeListItem1]
    type_id: int
    type_label: str


class PicTypeListItem(BaseModel):
    id: int
    name: str
    mi18n_name: str


class Data(BaseModel):
    list: List[ListItem]
    total: int
    type_list: List[TypeListItem]
    alert: bool
    alert_id: int
    timezone: int
    t: str
    pic_list: List[PicListItem]
    pic_total: int
    pic_type_list: List[PicTypeListItem]
    pic_alert: bool
    pic_alert_id: int
    static_sign: str


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

    def get_version_info(self):
        for lst in self.data.list:
            for i in lst.list:
                if "游戏优化及已知问题说明" in i.title:
                    return i

    def get_gacha_info(self):
        data: List[ListItem2] = []
        for i in self.data.pic_list:
            for j in i.type_list[0].list:
                if j.title.split("：").pop(0).endswith("跃迁"):
                    yield j
        return data

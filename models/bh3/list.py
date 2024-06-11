from __future__ import annotations

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
    start_time: str
    end_time: str
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


class Data(BaseModel):
    list: List[ListItem]
    total: int
    type_list: List[TypeListItem]
    alert: bool
    alert_id: int
    timezone: int
    t: str
    pic_list: List
    pic_total: int
    pic_type_list: List
    pic_alert: bool
    pic_alert_id: int
    static_sign: str


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

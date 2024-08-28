from __future__ import annotations

import datetime

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
    list: list[ListItem1]
    type_id: int
    type_label: str


class TypeListItem(BaseModel):
    id: int
    name: str
    mi18n_name: str


class Data(BaseModel):
    list: list[ListItem]
    total: int
    type_list: list[TypeListItem]
    alert: bool
    alert_id: int
    timezone: int
    t: str
    pic_list: list
    pic_total: int
    pic_type_list: list
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
                if "游戏更新修复与优化说明" in i.title:
                    return i
                if i.subtitle.endswith("版本更新说明"):
                    return i

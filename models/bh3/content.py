from __future__ import annotations

from pydantic import BaseModel


class ListItem(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    lang: str

    @property
    def image(self):
        return self.banner


class Data(BaseModel):
    list: list[ListItem]
    pic_list: list
    total: int
    pic_total: int


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

    def get_version_info(self):
        for i in self.data.list:
            if "游戏更新内容问题修复及优化说明" in i.title or "游戏更新内容公告" in i.subtitle:
                return i

    def get_gacha_info(self):
        return [i for i in self.data.list if "补给" in i.subtitle]

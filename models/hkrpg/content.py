from __future__ import annotations

from pydantic import BaseModel


class ListItem(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    lang: str


class PicListItem1(BaseModel):
    title: str
    img: str
    href_type: int
    href: str


class PicListItem(BaseModel):
    ann_id: int
    content_type: int
    title: str
    subtitle: str
    banner: str
    content: str
    lang: str
    img: str
    href_type: int
    href: str
    pic_list: list[PicListItem1]

    @property
    def image(self):
        return self.banner or self.img


class Data(BaseModel):
    pic_list: list[PicListItem]
    list: list[ListItem]
    total: int
    pic_total: int


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

    def get_version_info(self):
        for i in self.data.list:
            if "游戏优化及已知问题说明" in i.title:
                return i

    def get_gacha_info(self):
        return [i for i in self.data.pic_list if i.title.split("：")[0].endswith("跃迁")]

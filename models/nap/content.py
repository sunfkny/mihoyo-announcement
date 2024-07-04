from __future__ import annotations

from pydantic import BaseModel


class ListItem(BaseModel):
    ann_id: int
    title: str
    subtitle: str
    banner: str
    content: str
    lang: str


class Data(BaseModel):
    list: list[ListItem]
    total: int
    pic_list: list
    pic_total: int


class Model(BaseModel):
    retcode: int
    message: str
    data: Data

    def get_gacha_info(self):
        return [i for i in self.data.list if "调频" in i.subtitle]

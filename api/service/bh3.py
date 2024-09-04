import asyncio

import arrow
import bs4
import pydantic
from loguru import logger

import api.models.bh3.content
import api.models.bh3.list
from api.utils import request_async
from api.utils.timezone import get_tzinfo


async def get_ann_list():
    response_data = await request_async(
        "https://ann-api.mihoyo.com/common/bh3_cn/announcement/api/getAnnList",
        {
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "uid": "100000000",
        },
    )
    return api.models.bh3.list.Model.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://ann-static.mihoyo.com/common/bh3_cn/announcement/api/getAnnContent",
        {
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "uid": "100000000",
        },
    )
    return api.models.bh3.content.Model.model_validate(response_data)


class Bh3GachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    info_html: str | None


class Bh3Progress(pydantic.BaseModel):
    text: str | None
    percent: float | None


class Bh3Response(pydantic.BaseModel):
    progress: Bh3Progress
    gacha_info: list[Bh3GachaInfo]


async def get_bh3_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    progress_percent = None
    progress_text = None
    gacha_info: list[Bh3GachaInfo] = []

    if version_info:
        start_time = arrow.get(version_info.start_time, get_tzinfo(timezone))
        end_time = arrow.get(version_info.end_time, get_tzinfo(timezone))
        current_time = arrow.now("Asia/Shanghai")
        if start_time <= current_time <= end_time:
            progress_percent = (current_time - start_time) / (end_time - start_time)
            end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
            progress_text = f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）"

    for i in ann_content.get_gacha_info():
        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        info_header_text = content_soup.find(string=["开放时间", "补给信息"])
        info_header = info_header_text.parent if info_header_text else None
        info_element = info_header.find_next_sibling() if info_header else None
        if info_element and "活动期间内，以下所有装备均有一定概率获取；指定装备UP时间内，该装备的获取概率提升！" == info_element.text:
            info_element = info_element.find_next_sibling()

        info_html = None

        if info_element is not None:
            info_html = str(info_element)

        gacha_info.append(
            Bh3GachaInfo(
                ann_id=i.ann_id,
                title=i.title,
                image=i.image,
                content=i.content,
                info_html=info_html,
            )
        )

    return Bh3Response(
        progress=Bh3Progress(percent=progress_percent, text=progress_text),
        gacha_info=gacha_info,
    )

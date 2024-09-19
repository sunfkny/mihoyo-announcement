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
        elements = []
        open_time_header = content_soup.find(string=["开放时间"])
        logger.info(f"open_time_header {open_time_header}")
        if open_time_header and open_time_header.parent:
            elements.append(open_time_header.parent.find_next_sibling())

        info_header = content_soup.find(string=["补给信息"])
        if info_header and info_header.parent:
            info_header_next = info_header.parent.find_next_sibling()
            elements.append(info_header_next)

            if info_header_next and any(i in info_header_next.text for i in ["如下", "以下"]):
                elements.append(info_header_next.find_next_sibling())

        print(elements)
        elements = [i for i in elements if i]
        info_html = None
        if elements:
            info_html = "".join([str(i) for i in elements])

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

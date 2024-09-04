import asyncio
import re

import arrow
import bs4
import pydantic

import api.models.nap.content
import api.models.nap.list
from api.utils import request_async
from api.utils.timezone import get_tzinfo


async def get_ann_list():
    response_data = await request_async(
        "https://announcement-static.mihoyo.com/common/nap_cn/announcement/api/getAnnList",
        {
            "game": "nap",
            "game_biz": "nap_cn",
            "lang": "zh-cn",
            "bundle_id": "nap_cn",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": 40,
            "channel_id": 1,
            "uid": 10000000,
        },
    )

    return api.models.nap.list.Model.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://announcement-static.mihoyo.com/common/nap_cn/announcement/api/getAnnContent",
        {
            "game": "nap",
            "game_biz": "nap_cn",
            "lang": "zh-cn",
            "bundle_id": "nap_cn",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": 40,
            "channel_id": 1,
            "uid": 10000000,
        },
    )
    return api.models.nap.content.Model.model_validate(response_data)


class NapGachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    start_time: str | None
    end_time: str | None


class NapProgress(pydantic.BaseModel):
    text: str | None
    percent: float | None


class NapResponse(pydantic.BaseModel):
    progress: NapProgress
    gacha_info: list[NapGachaInfo]


async def get_nap_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    progress_percent = None
    progress_text = None
    gacha_info: list[NapGachaInfo] = []

    if version_info:
        start_time = arrow.get(version_info.start_time, get_tzinfo(timezone))
        end_time = arrow.get(version_info.end_time, get_tzinfo(timezone))
        current_time = arrow.now("Asia/Shanghai")
        if start_time <= current_time <= end_time:
            progress_percent = (current_time - start_time) / (end_time - start_time)
            end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
            progress_text = f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）"

    for i in ann_content.get_gacha_info():
        # 常驻频段
        stable_channel = "「热门卡司」调频说明"
        # 邦布频段
        bangboo_channel = "「卓越搭档」调频说明"
        # 永久频段
        permanent_channel_list = [
            stable_channel,
            bangboo_channel,
        ]
        if i.subtitle in permanent_channel_list:
            continue

        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        info_table_time = content_soup.select_one("table tr:nth-child(2) td")
        text = info_table_time.text if info_table_time else ""
        t = re.search(
            r"(?:(.*?后)|(.*?)（服务器时间）)~(.*?)（服务器时间）",
            text,
            re.MULTILINE,
        )
        start_time = None
        end_time = None
        match t.groups() if t else None:
            case [start_str, None, end_time]:
                end_time = arrow.get(end_time, tzinfo=get_tzinfo(timezone))
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                start_time = f"{start_str}"
                end_time = f"{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）"
            case [None, start_time, end_time]:
                start_time = arrow.get(start_time, tzinfo=get_tzinfo(timezone))
                end_time = arrow.get(end_time, tzinfo=get_tzinfo(timezone))
                start_time_humanize = start_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                start_time = f"{start_time:YYYY-MM-DD HH:mm:ss} （{start_time_humanize}）"
                end_time = f"{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）"

            case _:
                pass

        gacha_info.append(
            NapGachaInfo(
                ann_id=i.ann_id,
                title=i.subtitle,
                image=i.banner,
                content=i.content,
                start_time=start_time,
                end_time=end_time,
            )
        )

    return NapResponse(
        progress=NapProgress(percent=progress_percent, text=progress_text),
        gacha_info=gacha_info,
    )

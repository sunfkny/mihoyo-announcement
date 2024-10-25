import asyncio
import re

import arrow
import pydantic

import api.models.hkrpg.content
import api.models.hkrpg.list
from api.utils import request_async
from api.utils.timezone import get_tzinfo


async def get_ann_list():
    response_data = await request_async(
        "https://hkrpg-ann-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList",
        {
            "game": "hkrpg",
            "game_biz": "hkrpg_cn",
            "lang": "zh-cn",
            "bundle_id": "hkrpg_cn",
            "channel_id": "1",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": "70",
            "uid": "100000000",
        },
    )

    return api.models.hkrpg.list.Model.model_validate(response_data)


async def get_ann_content():
    response_data = await request_async(
        "https://hkrpg-ann-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnContent",
        {
            "game": "hkrpg",
            "game_biz": "hkrpg_cn",
            "lang": "zh-cn",
            "bundle_id": "hkrpg_cn",
            "channel_id": "1",
            "platform": "pc",
            "region": "prod_gf_cn",
            "level": "70",
            "uid": "100000000",
        },
    )
    return api.models.hkrpg.content.Model.model_validate(response_data)


class HkrpgGachaInfo(pydantic.BaseModel):
    ann_id: int
    title: str
    image: str
    content: str
    start_time: str | None
    end_time: str | None


class HkrpgProgress(pydantic.BaseModel):
    text: str | None
    percent: float | None


class HkrpgResponse(pydantic.BaseModel):
    progress: HkrpgProgress
    gacha_info: list[HkrpgGachaInfo]


async def get_hkrpg_gacha_info():
    ann_list, ann_content = await asyncio.gather(get_ann_list(), get_ann_content())
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    progress_percent = None
    progress_text = None
    gacha_info: list[HkrpgGachaInfo] = []

    if version_info:
        start_time = arrow.get(version_info.start_time, get_tzinfo(timezone))
        end_time = arrow.get(version_info.end_time, get_tzinfo(timezone))
        current_time = arrow.now("Asia/Shanghai")
        if start_time <= current_time <= end_time:
            progress_percent = (current_time - start_time) / (end_time - start_time)
            end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
            progress_text = f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）"

    for i in ann_content.get_gacha_info():
        t = re.search(
            r"(?:([0-9]+\.[0-9]版本更新后)|(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)).*?(\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}(?::\d{2})?)",
            i.content,
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
            HkrpgGachaInfo(
                ann_id=i.ann_id,
                title=i.title,
                image=i.image,
                content=i.content,
                start_time=start_time,
                end_time=end_time,
            )
        )

    return HkrpgResponse(
        progress=HkrpgProgress(percent=progress_percent, text=progress_text),
        gacha_info=gacha_info,
    )

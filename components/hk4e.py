import re

import arrow
import streamlit as st

import models.hk4e.content
import models.hk4e.list
from utils import cache_ttl, get_tzinfo, request


@st.cache_data(ttl=cache_ttl)
def get_ann_list():
    response_data = request(
        "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnList",
        {
            "game": "hk4e",
            "game_biz": "hk4e_cn",
            "lang": "zh-cn",
            "from_cloud_web": "1",
            "bundle_id": "hk4e_cn",
            "channel_id": "1",
            "level": "60",
            "platform": "pc",
            "region": "cn_gf01",
            "uid": "100000000",
        },
    )

    return models.hk4e.list.Model.model_validate(response_data)


@st.cache_data(ttl=cache_ttl)
def get_ann_content():
    response_data = request(
        "https://hk4e-api.mihoyo.com/common/hk4e_cn/announcement/api/getAnnContent",
        {
            "game": "hk4e",
            "game_biz": "hk4e_cn",
            "lang": "zh-cn",
            "from_cloud_web": "1",
            "bundle_id": "hk4e_cn",
            "channel_id": "1",
            "level": "60",
            "platform": "pc",
            "region": "cn_gf01",
            "uid": "100000000",
        },
    )
    return models.hk4e.content.Model.model_validate(response_data)


def hk4e():
    ann_list = get_ann_list()
    version_info = ann_list.get_version_info()
    timezone = ann_list.data.timezone
    if not version_info:
        st.warning("获取版本信息失败")
    else:
        start_time = arrow.get(version_info.start_time, tzinfo=get_tzinfo(timezone))
        end_time = arrow.get(version_info.end_time, tzinfo=get_tzinfo(timezone))
        current_time = arrow.now("Asia/Shanghai")
        if start_time <= current_time <= end_time:
            percent = (current_time - start_time) / (end_time - start_time)
            end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
            st.progress(percent, text=f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）")

    ann_content = get_ann_content()
    for i in ann_content.get_gacha_info():
        t = re.search(
            r'(?:([0-9]+\.[0-9]版本更新后)|&lt;t class="t_\w+"&gt;(.*?)&lt;\/t&gt;).*?&lt;t class="t_\w+"&gt;(.*?)&lt;\/t&gt;',
            i.content,
            re.MULTILINE,
        )
        st.image(image=i.image, caption=i.title)
        match t.groups() if t else None:
            case [start_str, None, end_time]:
                end_time = arrow.get(end_time, tzinfo=get_tzinfo(timezone))
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                st.markdown(f"开始时间：{start_str}")
                st.markdown(f"结束时间：{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）")
            case [None, start_time, end_time]:
                start_time = arrow.get(start_time, tzinfo=get_tzinfo(timezone))
                end_time = arrow.get(end_time, tzinfo=get_tzinfo(timezone))
                start_time_humanize = start_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                st.markdown(f"开始时间：{start_time:YYYY-MM-DD HH:mm:ss} （{start_time_humanize}）")
                st.markdown(f"结束时间：{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）")
            case _:
                st.text_area("content", value=i.content)

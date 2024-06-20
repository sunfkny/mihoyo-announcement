import re

import arrow
import streamlit as st

import models.hkrpg.content
import models.hkrpg.list
from components import Navbar
from utils import cache_ttl, request

Navbar()


@st.cache_data(ttl=cache_ttl)
def get_ann_list():
    response_data = request(
        "https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnList",
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

    return models.hkrpg.list.Model.model_validate(response_data)


@st.cache_data(ttl=cache_ttl)
def get_ann_content():
    response_data = request(
        "https://hkrpg-api.mihoyo.com/common/hkrpg_cn/announcement/api/getAnnContent",
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
    return models.hkrpg.content.Model.model_validate(response_data)


ann_content = get_ann_content()
for i in ann_content.get_gacha_info():
    t = re.search(
        r'(?:([0-9]+\.[0-9]版本更新后)| &lt;t class="t_\w+"&gt;(.*?)&lt;\/t&gt;) - &lt;t class="t_\w+"&gt;(.*?)&lt;\/t&gt;',
        i.content,
        re.MULTILINE,
    )
    with st.container(border=True):
        st.image(image=i.image, caption=i.title)
        match t.groups() if t else None:
            case [start_str, None, end_time]:
                end_time = arrow.get(end_time).to("Asia/Shanghai")
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                st.text(f"开始时间：{start_str}")
                st.text(f"结束时间：{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）")
            case [None, start_time, end_time]:
                start_time = arrow.get(start_time).to("Asia/Shanghai")
                end_time = arrow.get(end_time).to("Asia/Shanghai")
                start_time_humanize = start_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
                st.text(f"开始时间：{start_time:YYYY-MM-DD HH:mm:ss} （{start_time_humanize}）")
                st.text(f"结束时间：{end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}）")
            case _:
                st.text_area("content", value=i.content)

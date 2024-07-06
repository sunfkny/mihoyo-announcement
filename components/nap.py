import arrow
import bs4
import streamlit as st

import models.nap.content
import models.nap.list
from utils import cache_ttl, request
from utils.timezone import get_tzinfo


@st.cache_data(ttl=cache_ttl)
def get_ann_list():
    response_data = request(
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

    return models.nap.list.Model.model_validate(response_data)


@st.cache_data(ttl=cache_ttl)
def get_ann_content():
    response_data = request(
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
    return models.nap.content.Model.model_validate(response_data)


def nap():
    ann_list = get_ann_list()
    timezone = ann_list.data.timezone
    version_info = ann_list.get_version_info()
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
        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        info_table_time = content_soup.select_one("table tr:nth-child(2) td")
        text = info_table_time.text if info_table_time else None
        if text:
            st.image(image=i.banner, caption=i.subtitle)
            st.markdown(text)
        else:
            # 常驻频段
            stable_channel = "「热门卡司」调频说明"
            # 邦布频段
            bangboo_channel = "「卓越搭档」调频说明"
            # 永久频段
            permanent_channel_list = [
                stable_channel,
                bangboo_channel,
            ]
            if i.subtitle not in permanent_channel_list:
                st.image(image=i.banner, caption=i.subtitle)
                st.text_area("content", value=i.content)

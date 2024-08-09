import arrow
import bs4
import streamlit as st

import models.bh3.content
import models.bh3.list
from utils import cache_ttl, get_tzinfo, request


@st.cache_data(ttl=cache_ttl)
def get_ann_list():
    response_data = request(
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
    return models.bh3.list.Model.model_validate(response_data)


@st.cache_data(ttl=cache_ttl)
def get_ann_content():
    response_data = request(
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
    return models.bh3.content.Model.model_validate(response_data)


def bh3():
    ann_list = get_ann_list()
    timezone = ann_list.data.timezone
    version_info = ann_list.get_version_info()
    if not version_info:
        st.warning("获取版本信息失败")
    else:
        start_time = arrow.get(version_info.start_time, get_tzinfo(timezone))
        end_time = arrow.get(version_info.end_time, get_tzinfo(timezone))
        current_time = arrow.now("Asia/Shanghai")
        if start_time <= current_time <= end_time:
            percent = (current_time - start_time) / (end_time - start_time)
            end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
            st.progress(percent, text=f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）")

    ann_content = get_ann_content()
    for i in ann_content.get_gacha_info():
        st.image(image=i.image, caption=i.title)

        content_soup = bs4.BeautifulSoup(i.content, "html.parser")
        info_header_text = content_soup.find(string=["开放时间", "补给信息"])
        info_header = info_header_text.parent if info_header_text else None
        info_element = info_header.find_next_sibling() if info_header else None
        if info_element and "活动期间内，以下所有装备均有一定概率获取；指定装备UP时间内，该装备的获取概率提升！" == info_element.text:
            info_element = info_element.find_next_sibling()

        if info_element is not None:
            st.html(str(info_element))
        else:
            st.text_area("content", value=i.content)

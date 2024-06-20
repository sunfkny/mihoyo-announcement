import re

import arrow
import bs4
import streamlit as st

import models.bh3.content
import models.bh3.list
from utils import cache_ttl, get_tzinfo, request


@st.cache_data(ttl=cache_ttl)
def get_ann_list():
    response_data = request(
        "https://api-takumi.mihoyo.com/common/bh3_cn/announcement/api/getAnnList",
        {
            "auth_appid": "announcement",
            "authkey_ver": "1",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "sdk_presentation_style": "fullscreen",
            "sdk_screen_transparent": "true",
            "sign_type": "2",
            "uid": "100000000",
        },
    )

    return models.bh3.list.Model.model_validate(response_data)


@st.cache_data(ttl=cache_ttl)
def get_ann_content():
    response_data = request(
        "https://api-takumi.mihoyo.com/common/bh3_cn/announcement/api/getAnnContent",
        {
            "auth_appid": "announcement",
            "authkey_ver": "1",
            "bundle_id": "bh3_cn",
            "channel_id": "14",
            "game": "bh3",
            "game_biz": "bh3_cn",
            "lang": "zh-cn",
            "level": "88",
            "platform": "pc",
            "region": "bb01",
            "sdk_presentation_style": "fullscreen",
            "sdk_screen_transparent": "true",
            "sign_type": "2",
            "uid": "100000000",
        },
    )
    return models.bh3.content.Model.model_validate(response_data)


def bh3():
    ann_list = get_ann_list()
    version_info = ann_list.get_version_info()
    if not version_info:
        st.warning("获取版本信息失败")
        return
    timezone = ann_list.data.timezone
    start_time = arrow.get(version_info.start_time,get_tzinfo(timezone))
    end_time = arrow.get(version_info.end_time,get_tzinfo(timezone))
    current_time = arrow.now("Asia/Shanghai")
    if start_time <= current_time <= end_time:
        percent = (current_time - start_time) / (end_time - start_time)
        end_time_humanize = end_time.humanize(locale="zh", granularity=["day", "hour", "minute"])
        st.progress(percent, text=f"{start_time:YYYY-MM-DD HH:mm:ss} ~ {end_time:YYYY-MM-DD HH:mm:ss} （{end_time_humanize}结束）")
    ann_content = get_ann_content()
    for i in ann_content.get_gacha_info():
        content_bs = bs4.BeautifulSoup(i.content, "html.parser")
        content_images = content_bs.find_all("img")
        content_text = content_bs.get_text()

        st.image(image=i.image, caption=i.title)
        for image in content_images:
            st.image(image=image["src"])
        if not content_images:
            match_time = re.search(r"开放时间(.*?)开放等级", content_text, re.MULTILINE)
            if match_time:
                st.markdown(match_time.group(1))
            else:
                st.text_area("content", value=i.content)

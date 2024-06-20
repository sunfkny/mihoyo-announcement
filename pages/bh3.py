import re

import bs4
import streamlit as st

import models.bh3.content
import models.bh3.list
from components import Navbar
from utils import cache_ttl, request

Navbar()


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


ann_content = get_ann_content()
for i in ann_content.get_gacha_info():
    content_bs = bs4.BeautifulSoup(i.content, "html.parser")
    content_images = content_bs.find_all("img")
    content_text = content_bs.get_text()

    with st.container(border=True):
        st.image(image=i.image, caption=i.title)
        for image in content_images:
            st.image(image=image["src"])
        if not content_images:
            match_time = re.search(r"开放时间(.*?)开放等级", content_text, re.MULTILINE)
            if match_time:
                st.text(match_time.group(1))
            else:
                st.text_area("content", value=i.content)

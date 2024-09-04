import streamlit as st

import api.models.bh3.content
import api.models.bh3.list
import api.service.bh3


async def get_bh3_gacha_info():
    return await api.service.bh3.get_bh3_gacha_info()


async def bh3():
    info = await get_bh3_gacha_info()
    if info.progress.text is None or info.progress.percent is None:
        st.warning("获取版本信息失败")
    else:
        st.progress(info.progress.percent, text=info.progress.text)

    for i in info.gacha_info:
        st.image(image=i.image, caption=i.title)

        if i.info_html:
            st.html(i.info_html)
        else:
            st.text_area("content", value=i.content)

import streamlit as st
from aiocache import Cache, cached

import api.models.hk4e.content
import api.models.hk4e.list
import api.service.hk4e


async def get_hk4e_gacha_info():
    return await api.service.hk4e.get_hk4e_gacha_info()


async def hk4e():
    info = await get_hk4e_gacha_info()
    if info.progress.text is None or info.progress.percent is None:
        st.warning("获取版本信息失败")
    else:
        st.progress(info.progress.percent, text=info.progress.text)

    for i in info.gacha_info:
        st.image(image=i.image, caption=i.title)

        if i.start_time is not None and i.end_time is not None:
            st.markdown(f"开始时间：{i.start_time}")
            st.markdown(f"结束时间：{i.end_time}")
        else:
            st.text_area("content", value=i.content)

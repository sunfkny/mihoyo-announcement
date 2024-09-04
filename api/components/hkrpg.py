import streamlit as st

import api.models.hkrpg.content
import api.models.hkrpg.list
import api.service.hkrpg


async def get_hkrpg_gacha_info():
    return await api.service.hkrpg.get_hkrpg_gacha_info()


async def hkrpg():
    info = await get_hkrpg_gacha_info()
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

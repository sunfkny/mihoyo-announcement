import streamlit as st

from components import Navbar

Navbar()
st.markdown("""
请从左侧菜单选择要查看的游戏

公告接口来自官方公告网页

[崩坏3公告](https://webstatic.mihoyo.com/bh3/announcement/index.html?auth_appid=announcement&authkey_ver=1&bundle_id=bh3_cn&channel_id=14&game=bh3&game_biz=bh3_cn&lang=zh-cn&level=88&platform=pc&region=android01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=100000000)

[原神公告](https://webstatic.mihoyo.com/hk4e/announcement/index.html?from_cloud_web=1&auth_appid=announcement&authkey_ver=1&bundle_id=hk4e_cn&channel_id=1&game=hk4e&game_biz=hk4e_cn&lang=zh-cn&level=60&platform=pc&region=cn_gf01&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&uid=100000000)

[崩坏：星穹铁道公告](https://webstatic.mihoyo.com/hkrpg/announcement/index.html?auth_appid=announcement&authkey_ver=1&bundle_id=hkrpg_cn&channel_id=1&game=hkrpg&game_biz=hkrpg_cn&lang=zh-cn&platform=pc&region=prod_gf_cn&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&sign_type=2&level=70&uid=100000000)
""")

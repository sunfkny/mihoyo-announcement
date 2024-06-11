from announcement import Bh3Announcement, Hk4eAnnouncement, HkrpgAnnouncement
import streamlit as st
import datetime


@st.cache_resource
def get_bh3_gacha_info():
    return list(Bh3Announcement().get_gacha_info())


@st.cache_resource
def get_hk4e_gacha_info():
    return list(Hk4eAnnouncement().get_gacha_info())


@st.cache_resource
def get_hkrpg_gacha_info():
    return list(HkrpgAnnouncement().get_gacha_info())


def get_humanize(dt):
    # return arrow.get(dt).humanize(locale="zh", only_distance=True, granularity="day")
    diff = datetime.datetime.fromisoformat(dt) - datetime.datetime.now().replace(microsecond=0)
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"剩余 {days} 天 {hours} 小时 {minutes} 分钟"


st.title("崩坏3")
for i in get_bh3_gacha_info():
    st.image(i.banner, caption=f"{i.title} - {get_humanize(i.end_time)}")

st.title("原神")
for i in get_hk4e_gacha_info():
    st.image(i.banner, caption=f"{i.title} - {get_humanize(i.end_time)}")

st.title("崩坏：星穹铁道")
for i in get_hkrpg_gacha_info():
    st.image(i.img, caption=f"{i.title} - {get_humanize(i.end_time)}")

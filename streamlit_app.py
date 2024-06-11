from announcement import Bh3Announcement, Hk4eAnnouncement, HkrpgAnnouncement
import streamlit as st
import datetime


@st.cache_resource
def get_bh3():
    return Bh3Announcement()


@st.cache_resource
def get_hk4e():
    return Hk4eAnnouncement()


@st.cache_resource
def get_hkrpg():
    return HkrpgAnnouncement()


@st.cache_resource(ttl=60)
def get_bh3_gacha_info():
    return list(get_bh3().get_gacha_info())


@st.cache_resource(ttl=60)
def get_hk4e_gacha_info():
    return list(get_hk4e().get_gacha_info())


@st.cache_resource(ttl=60)
def get_hkrpg_gacha_info():
    return list(get_hkrpg().get_gacha_info())


@st.cache_resource(ttl=60)
def get_bh3_version_info():
    return get_bh3().get_version_info()


@st.cache_resource(ttl=60)
def get_hk4e_version_info():
    return get_hk4e().get_version_info()


@st.cache_resource(ttl=60)
def get_hkrpg_version_info():
    return get_hkrpg().get_version_info()


def get_humanize(dt: datetime.datetime):
    diff = dt - datetime.datetime.now()
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"剩余 {days} 天 {hours} 小时 {minutes} 分钟"


def calculate_progress_percentage(
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    current_time: datetime.datetime,
):
    if start_time > end_time:
        start_time, end_time = end_time, start_time
    if current_time < start_time:
        return 0
    if current_time > end_time:
        return 100
    diff = end_time - start_time
    total_seconds = diff.total_seconds()
    elapsed_seconds = (current_time - start_time).total_seconds()
    return int(elapsed_seconds / total_seconds * 100)


current_time = datetime.datetime.now()

st.title("崩坏3")
bh3_version_info = get_bh3_version_info()
if bh3_version_info is not None:
    st.caption(f"{bh3_version_info.start_time} - {bh3_version_info.end_time}")
    st.progress(
        calculate_progress_percentage(
            start_time=bh3_version_info.start_time,
            end_time=bh3_version_info.end_time,
            current_time=current_time,
        )
    )
for i in get_bh3_gacha_info():
    st.image(i.banner, caption=f"{i.title} - {get_humanize(i.end_time)}")

st.title("原神")
hk4e_version_info = get_hk4e_version_info()
if hk4e_version_info is not None:
    st.caption(f"{hk4e_version_info.start_time} - {hk4e_version_info.end_time}")
    st.progress(
        calculate_progress_percentage(
            start_time=hk4e_version_info.start_time,
            end_time=hk4e_version_info.end_time,
            current_time=current_time,
        )
    )
for i in get_hk4e_gacha_info():
    st.image(i.banner, caption=f"{i.title} - {get_humanize(i.end_time)}")

st.title("崩坏：星穹铁道")
hkrpg_version_info = get_hkrpg_version_info()
if hkrpg_version_info is not None:
    st.caption(f"{hkrpg_version_info.start_time} - {hkrpg_version_info.end_time}")
    st.progress(
        calculate_progress_percentage(
            start_time=hkrpg_version_info.start_time,
            end_time=hkrpg_version_info.end_time,
            current_time=current_time,
        )
    )
for i in get_hkrpg_gacha_info():
    st.image(i.img, caption=f"{i.title} - {get_humanize(i.end_time)}")

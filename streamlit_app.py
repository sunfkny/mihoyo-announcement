import datetime
from collections.abc import Callable

import arrow
import streamlit as st

from announcement import Bh3Announcement, Hk4eAnnouncement, HkrpgAnnouncement
from models.bh3 import list as bh3_list
from models.hk4e import list as hk4e_list
from models.hkrpg import list as hkrpg_list

api_ttl = 10


@st.cache_resource(ttl=api_ttl)
def get_bh3_ann_list():
    return Bh3Announcement().get_ann_list()


@st.cache_resource(ttl=api_ttl)
def get_hk4e_ann_list():
    return Hk4eAnnouncement().get_ann_list()


@st.cache_resource(ttl=api_ttl)
def get_hkrpg_ann_list():
    return HkrpgAnnouncement().get_ann_list()


current_time = arrow.now()


def get_humanize(end_time: datetime.datetime, timezone: int):
    dt = arrow.get(end_time, tzinfo=f"UTC{timezone:+03d}")
    if dt < current_time:
        return "已结束"
    diff = dt - current_time
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"剩余 {days} 天 {hours} 小时 {minutes} 分钟"


def calculate_progress_percentage(
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    timezone: int,
):
    tzinfo = arrow.parser.TzinfoParser.parse(f"{timezone:>02}")
    current_time_naive = current_time.to(tzinfo).naive
    if start_time > end_time:
        start_time, end_time = end_time, start_time
    if current_time_naive < start_time:
        return 0
    if current_time_naive > end_time:
        return 100
    diff = end_time - start_time
    total_seconds = diff.total_seconds()
    elapsed_seconds = (current_time_naive - start_time).total_seconds()
    return int(elapsed_seconds / total_seconds * 100)


GameListModel = bh3_list.Model | hk4e_list.Model | hkrpg_list.Model
games: dict[str, Callable[[], GameListModel]] = {
    "崩坏3": get_bh3_ann_list,
    "原神": get_hk4e_ann_list,
    "崩坏：星穹铁道": get_hkrpg_ann_list,
}

for game_name, get_list in games.items():
    st.title(game_name)
    lst = get_list()
    v = lst.get_version_info()
    timezone = lst.data.timezone
    if v is None:
        st.warning("未获取到版本信息")
    else:
        end_time_humanize = get_humanize(end_time=v.end_time, timezone=timezone)
        st.progress(
            value=calculate_progress_percentage(
                start_time=v.start_time,
                end_time=v.end_time,
                timezone=timezone,
            ),
            text=f"{v.start_time} ~ {v.end_time} （{end_time_humanize}）",
        )
    gacha_info = lst.get_gacha_info()
    for i in gacha_info:
        with st.container(border=True):
            image = i.img if isinstance(i, hkrpg_list.ListItem2) else i.banner
            st.image(image=image, caption=i.title)

            banner_is_preview = False
            if v is not None:
                banner_is_preview = datetime.timedelta() < v.end_time - i.start_time < datetime.timedelta(days=1)

            if banner_is_preview:
                st.caption(f"版本更新后 ~ {i.end_time}")
            else:
                end_time_humanize = get_humanize(end_time=i.end_time, timezone=timezone)
                st.progress(
                    value=calculate_progress_percentage(
                        start_time=i.start_time,
                        end_time=i.end_time,
                        timezone=timezone,
                    ),
                    text=f"{i.start_time} ~ {i.end_time} （{end_time_humanize}）",
                )

import streamlit as st

from api.components.bh3 import bh3
from api.components.hk4e import hk4e
from api.components.hkrpg import hkrpg
from api.components.nap import nap

with st.expander("崩坏3", expanded=False):
    bh3()
with st.expander("原神", expanded=False):
    hk4e()
with st.expander("崩坏：星穹铁道", expanded=False):
    hkrpg()
with st.expander("绝区零", expanded=False):
    nap()

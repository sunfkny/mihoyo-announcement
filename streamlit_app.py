import streamlit as st

from components.bh3 import bh3
from components.hk4e import hk4e
from components.hkrpg import hkrpg

with st.expander("崩坏3", expanded=True):
    bh3()
with st.expander("原神", expanded=True):
    hk4e()
with st.expander("崩坏：星穹铁道", expanded=True):
    hkrpg()

import streamlit as st

monitoring_page = st.Page("streamlit_monitoring.py", title="Monitoring", icon="🌦️")
create_page = st.Page("streamlit_add_data.py", title="Add Data", icon="📚")
lookalike_page = st.Page("streamlit_lookalike.py", title="Who is My Lookalike?", icon="🎭")
pg = st.navigation([monitoring_page, create_page, lookalike_page])
st.set_page_config(page_title="Datalakes Final Project", page_icon="📦")
pg.run()
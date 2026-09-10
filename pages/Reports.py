import streamlit as st
import pandas as pd
from utils.helpers import load_json


def render():
    st.title('Reports Center')
    projects = pd.DataFrame(load_json('projects.json'))
    if projects.empty:
        st.info('No data to report.')
        return

    st.dataframe(projects, use_container_width=True, hide_index=True)
    st.download_button('Export CSV', projects.to_csv(index=False), file_name='aily_reports.csv', mime='text/csv')
    st.download_button('Export Excel', projects.to_excel('aily_reports.xlsx', index=False), file_name='aily_reports.xlsx')

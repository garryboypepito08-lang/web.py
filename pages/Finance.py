import streamlit as st
import pandas as pd
from utils.helpers import load_json


def render():
    st.title('Financial Operations')
    projects = load_json('projects.json')
    project_df = pd.DataFrame(projects)
    total_budget = project_df['budget'].sum() if not project_df.empty else 0
    remaining = total_budget * 0.42

    col1, col2, col3 = st.columns(3)
    col1.metric('Income', f'PHP {total_budget:,.2f}')
    col2.metric('Expenses', f'PHP {total_budget * 0.58:,.2f}')
    col3.metric('Remaining Balance', f'PHP {remaining:,.2f}')

    st.subheader('Budget Usage')
    st.bar_chart(project_df[['budget']].rename(columns={'budget': 'Budget'}))

    st.subheader('Cash Flow')
    flow_df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Income': [850000, 980000, 1100000, 1050000, 1200000],
        'Expenses': [600000, 720000, 760000, 800000, 910000],
    })
    st.line_chart(flow_df.set_index('Month'))

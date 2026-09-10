import streamlit as st
from pathlib import Path
from components.sidebar import render_sidebar
from pages.Dashboard import render as render_dashboard
from pages.Projects import render as render_projects
from pages.Materials import render as render_materials
from pages.Employees import render as render_employees
from pages.Payroll import render as render_payroll
from pages.Finance import render as render_finance
from pages.Reports import render as render_reports
from pages.Admin import render as render_admin
from pages.WordPuzzle import render as render_word_puzzle

st.set_page_config(page_title='AILY HOUSE PROJECT', page_icon='🏗️', layout='wide')

APP_DIR = Path(__file__).resolve().parent
CSS_PATH = APP_DIR / 'assets' / 'style.css'
css = CSS_PATH.read_text(encoding='utf-8')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

page = st.query_params.get('page')
if page:
    st.session_state.page = page

render_sidebar()

pages = {
    'Dashboard': render_dashboard,
    'Project Overview': render_projects,
    'Project Control': render_projects,
    'Financial Operations': render_finance,
    'Payroll Operations': render_payroll,
    'Administration': render_admin,
    'Word Puzzle': render_word_puzzle,
}

if st.session_state.page in pages:
    pages[st.session_state.page]()
else:
    render_dashboard()

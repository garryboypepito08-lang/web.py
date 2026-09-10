import streamlit as st
from utils.helpers import load_json, save_json, format_currency


def render():
    st.title("Project Overview")
    projects = load_json('projects.json')

    with st.container():
        col1, col2, col3 = st.columns([1.2, 1, 1])
        with col1:
            search = st.text_input('Search project', placeholder='Search projects...')
        with col2:
            status_filter = st.selectbox('Filter', ['All', 'In Progress', 'On Hold', 'Not Started'])
        with col3:
            sort_by = st.selectbox('Sort by', ['Name', 'Progress', 'Start Date'])

    filtered = projects
    if search:
        filtered = [p for p in filtered if search.lower() in p['name'].lower() or search.lower() in p['location'].lower()]
    if status_filter != 'All':
        filtered = [p for p in filtered if p['status'] == status_filter]
    if sort_by == 'Progress':
        filtered = sorted(filtered, key=lambda p: p['progress'], reverse=True)
    elif sort_by == 'Start Date':
        filtered = sorted(filtered, key=lambda p: p['start_date'])
    else:
        filtered = sorted(filtered, key=lambda p: p['name'])

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    if st.button('Add Project'):
        new_project = {
            'id': len(projects) + 1,
            'name': 'New Project',
            'location': 'New Location',
            'start_date': '2025-07-01',
            'status': 'Not Started',
            'progress': 0,
            'budget': 1000000,
        }
        projects.append(new_project)
        save_json('projects.json', projects)
        st.success('Project added.')

    if st.button('Export CSV'):
        import pandas as pd
        df = pd.DataFrame(filtered)
        csv = df.to_csv(index=False)
        st.download_button('Download CSV', csv, file_name='projects.csv', mime='text/csv')

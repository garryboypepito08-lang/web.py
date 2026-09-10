import streamlit as st


def render():
    st.title('Administration')
    st.subheader('User Management')
    users = [
        {'name': 'Administrator', 'role': 'Admin', 'status': 'Active'},
        {'name': 'Finance Lead', 'role': 'Finance', 'status': 'Active'},
        {'name': 'Project Manager', 'role': 'Manager', 'status': 'Active'},
    ]
    st.dataframe(users, use_container_width=True, hide_index=True)

    st.subheader('Settings')
    theme = st.selectbox('Theme', ['Emerald Green', 'Dark Night', 'Classic'])
    st.checkbox('Enable notifications')
    st.checkbox('Auto-refresh dashboard')
    st.button('Create backup')
    st.button('Restore backup')

import streamlit as st
from utils.helpers import load_json, save_json


def render():
    st.title('Employee Management')
    employees = load_json('employees.json')
    st.dataframe(employees, use_container_width=True, hide_index=True)

    with st.form('employee_form'):
        name = st.text_input('Employee name')
        position = st.text_input('Position')
        department = st.text_input('Department')
        attendance = st.number_input('Attendance %', min_value=0, max_value=100)
        submitted = st.form_submit_button('Add employee')

    if submitted:
        employees.append({
            'id': len(employees) + 1,
            'name': name,
            'position': position,
            'department': department,
            'attendance': int(attendance),
            'status': 'Active',
        })
        save_json('employees.json', employees)
        st.success('Employee added.')

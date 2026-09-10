import streamlit as st
from utils.helpers import load_json, save_json


def render():
    st.title('Payroll Operations')
    payroll = load_json('payroll.json')
    st.dataframe(payroll, use_container_width=True, hide_index=True)

    with st.form('payroll_form'):
        employee_name = st.text_input('Employee name')
        basic_pay = st.number_input('Basic pay', min_value=0.0, step=500.0)
        overtime = st.number_input('Overtime', min_value=0.0, step=100.0)
        deductions = st.number_input('Deductions', min_value=0.0, step=100.0)
        submitted = st.form_submit_button('Save payslip')

    if submitted:
        net = basic_pay + overtime - deductions
        payroll.append({
            'employee_id': len(payroll) + 1,
            'name': employee_name,
            'basic_pay': float(basic_pay),
            'overtime': float(overtime),
            'deductions': float(deductions),
            'net_pay': float(net),
        })
        save_json('payroll.json', payroll)
        st.success(f'Pay slip saved. Net pay: PHP {net:,.2f}')

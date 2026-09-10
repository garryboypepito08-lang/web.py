import streamlit as st
from utils.helpers import load_json, save_json


def render():
    st.title('Material Management')
    materials = load_json('materials.json')
    df = st.dataframe(materials, use_container_width=True, hide_index=True)

    with st.form('material_form'):
        name = st.text_input('Material name')
        supplier = st.text_input('Supplier')
        stock = st.number_input('Stock', min_value=0)
        unit_cost = st.number_input('Unit cost', min_value=0.0, step=10.0)
        low_stock = st.number_input('Low stock alert', min_value=0)
        submitted = st.form_submit_button('Save material')

    if submitted:
        materials.append({
            'id': len(materials) + 1,
            'name': name,
            'supplier': supplier,
            'stock': int(stock),
            'unit_cost': float(unit_cost),
            'low_stock': int(low_stock),
        })
        save_json('materials.json', materials)
        st.success('Material saved.')

    low_stock_items = [m for m in materials if m['stock'] <= m['low_stock']]
    if low_stock_items:
        st.warning(f'{len(low_stock_items)} material item(s) need restocking.')

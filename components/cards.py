import streamlit as st


def render_kpi_card(icon, label, value, delta, accent='green'):
    st.markdown(
        f"""
        <div class='glass-card kpi-card' style='padding:18px 18px 14px; min-height: 145px; margin-bottom: 10px;'>
            <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom: 18px;'>
                <div style='width:42px;height:42px;border-radius:12px;background:rgba(0,255,153,0.08);border:1px solid rgba(0,255,153,0.2);display:flex;align-items:center;justify-content:center;color:#7ef5c2;font-size:1.3rem;'>{icon}</div>
                <div style='font-size:0.75rem; color:#90f5d4; font-weight:700;'>{delta}</div>
            </div>
            <div class='metric-label'>{label}</div>
            <div class='metric-number' style='margin-top:10px;'>{value}</div>
            <div style='margin-top:14px; background: rgba(255,255,255,0.04); border-radius: 999px; overflow:hidden; height:8px;'>
                <div style='width: 72%; height:100%; border-radius:999px; background: linear-gradient(90deg, #00ff99, #00e676);'></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(status):
    status_lower = status.lower().replace(' ', '')
    if status_lower == 'inprogress':
        css = 'status-badge status-inprogress'
    elif status_lower == 'onhold':
        css = 'status-badge status-onhold'
    else:
        css = 'status-badge status-notstarted'
    return f'<span class="{css}">{status}</span>'

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from zoneinfo import ZoneInfo

from components.cards import render_kpi_card
from components.charts import make_status_donut
from utils.helpers import load_json


def navigate(page_name):
    st.session_state.page = page_name
    st.query_params['page'] = page_name
    st.rerun()


def render():
    try:
        projects = load_json('projects.json')
        materials = load_json('materials.json')
        employees = load_json('employees.json')
    except Exception:
        projects, materials, employees = [], [], []

    total_projects = len(projects)
    total_materials = sum(item.get('stock', 0) for item in materials)
    total_employees = len(employees)
    progress_avg = round(sum(item.get('progress', 0) for item in projects) / total_projects, 1) if total_projects else 0

    now = datetime.now(ZoneInfo('Asia/Manila'))
    clock_text = now.strftime('%I:%M:%S %p')
    date_text = now.strftime('%a, %b %d, %Y')

    st.markdown("<div class='top-nav-shell'>", unsafe_allow_html=True)
    nav_cols = st.columns([0.7, 3.6, 0.75, 0.9, 1.4, 1.15])
    with nav_cols[0]:
        st.markdown("<div class='nav-icon'>☰</div>", unsafe_allow_html=True)
    with nav_cols[1]:
        st.text_input('Search dashboard', label_visibility='collapsed', placeholder='Search projects, materials, teams...', key='dashboard_search')
    with nav_cols[2]:
        if st.button('🔔', key='dashboard_notifications', help='Notifications', use_container_width=True):
            pass
    with nav_cols[3]:
        if st.button('⚡', key='dashboard_quick', help='Quick actions', use_container_width=True):
            pass
    with nav_cols[4]:
        st.markdown(
            f"""
            <div class='profile-pill'>
                <div class='profile-avatar'>A</div>
                <div>
                    <div class='profile-name'>Administrator</div>
                    <div class='profile-status'>Online</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nav_cols[5]:
        st.markdown(
            f"""
            <div class='live-panel'>
                <div class='live-status'><span class='online-dot'></span> Online</div>
                <div class='live-clock'>{clock_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='hero-panel'>
            <div class='hero-glow'></div>
            <div class='hero-content'>
                <div class='eyebrow'>Executive command center</div>
                <h1>Good Evening, <span>Administrator</span></h1>
                <div class='hero-meta'>{date_text} • {clock_text}</div>
                <p>“Building today for a better tomorrow.”</p>
            </div>
            <div class='hero-kpis'>
                <div class='hero-chip'><span>Live status</span><strong>Stable</strong></div>
                <div class='hero-chip'><span>Projects</span><strong>{total_projects}</strong></div>
                <div class='hero-chip'><span>Progress</span><strong>{progress_avg}%</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        render_kpi_card('🏗', 'Total Projects', str(total_projects), '+12.4%')
    with kpi_cols[1]:
        render_kpi_card('📦', 'Materials', str(total_materials), '+8.1%')
    with kpi_cols[2]:
        render_kpi_card('👥', 'Employees', str(total_employees), '+4.7%')
    with kpi_cols[3]:
        render_kpi_card('📈', 'Project Progress', f'{progress_avg}%', '+3.2%')

    analytics_left, analytics_right = st.columns([1.8, 1.15])

    with analytics_left:
        st.markdown("<div class='section-title'>Project Performance</div>", unsafe_allow_html=True)
        week_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        week_values = [42, 48, 57, 63, 71, 84]
        line_fig = px.line(
            x=week_labels,
            y=week_values,
            template='plotly_dark',
            markers=True,
            line_shape='spline',
            range_y=[0, 100],
        )
        line_fig.update_traces(line=dict(color='#00FF99', width=3), marker=dict(size=7, color='#66FFC4'))
        line_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=10, t=10, b=20),
            font=dict(color='#E7FFF2', family='Eurostile Extended, Eurostile, Arial Narrow, sans-serif'),
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.15, xanchor='left', x=0),
        )
        st.plotly_chart(line_fig, use_container_width=True, config={'displayModeBar': False})

    with analytics_right:
        st.markdown("<div class='section-title'>Project Distribution</div>", unsafe_allow_html=True)
        values = {"In Progress": 3, "On Hold": 1, "Not Started": 1}
        donut_fig = make_status_donut(values)
        st.plotly_chart(donut_fig, use_container_width=True, config={'displayModeBar': False})

        metric_cols = st.columns(2)
        with metric_cols[0]:
            st.metric('Active', '14', '↑ 6%')
        with metric_cols[1]:
            st.metric('Pending', '5', '↓ 2%')

    project_df = pd.DataFrame(projects)
    project_df = project_df.copy()
    if not project_df.empty:
        project_df['status'] = project_df.get('status', 'In Progress').fillna('In Progress')
        project_df['progress'] = pd.to_numeric(project_df.get('progress', 0), errors='coerce').fillna(0).astype(int)

    control_cols = st.columns([2.4, 1.2, 1.1])
    with control_cols[0]:
        st.markdown("<div class='section-title'>Project Command Center</div>", unsafe_allow_html=True)
    with control_cols[1]:
        status_filter = st.selectbox('Filter', ['All', 'In Progress', 'On Hold', 'Not Started'], index=0, key='dashboard_status_filter')
    with control_cols[2]:
        sort_option = st.selectbox('Sort', ['Progress', 'Project Name', 'Start Date'], index=0, key='dashboard_sort')

    if project_df.empty:
        st.info('No project data available.')
    else:
        if status_filter != 'All':
            project_df = project_df[project_df['status'] == status_filter]
        if sort_option == 'Project Name':
            project_df = project_df.sort_values('name', ascending=True)
        elif sort_option == 'Start Date':
            project_df = project_df.sort_values('start_date', ascending=False)
        else:
            project_df = project_df.sort_values('progress', ascending=False)

        display_df = project_df[['name', 'location', 'start_date', 'status', 'progress']].copy()
        display_df.columns = ['Project Name', 'Location', 'Start Date', 'Status', 'Progress']
        display_df['Progress'] = display_df['Progress'].astype(str) + '%'
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    timeline_cols = st.columns([1.2, 2.1])
    with timeline_cols[0]:
        st.markdown("<div class='section-title'>Activity Timeline</div>", unsafe_allow_html=True)
    with timeline_cols[1]:
        st.markdown("<div class='muted-note'>Construction milestones and system updates</div>", unsafe_allow_html=True)

    activity_items = [
        ('📦', 'Material delivery complete', '2h ago', 'Materials', 'emerald'),
        ('💸', 'Payroll batch processed', '4h ago', 'Payroll', 'cyan'),
        ('🏗', 'Site inspection approved', '6h ago', 'Operations', 'amber'),
        ('👥', 'New project engineer assigned', '9h ago', 'HR', 'violet'),
        ('💰', 'Budget review submitted', '1d ago', 'Finance', 'slate'),
    ]

    timeline_html = "<div class='timeline'>"
    for icon, title, time_value, tag, tone in activity_items:
        timeline_html += f"""
        <div class='timeline-item {tone}'>
            <div class='timeline-icon'>{icon}</div>
            <div class='timeline-content'>
                <div class='timeline-head'>
                    <strong>{title}</strong>
                    <span class='timeline-tag'>{tag}</span>
                </div>
                <div class='timeline-time'>{time_value}</div>
            </div>
        </div>
        """
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

    widget_cols = st.columns(4)
    widgets = [
        ('Live System Status', 'ONLINE', '99.9% uptime', 'emerald'),
        ('Active Users', '42', 'Across 6 teams', 'cyan'),
        ('Storage Usage', '68%', '12.4 TB left', 'amber'),
        ('Upcoming Deadlines', '04', 'This week', 'violet'),
    ]
    for idx, col in enumerate(widget_cols):
        label, value, note, tone = widgets[idx]
        with col:
            st.markdown(
                f"""
                <div class='widget-card {tone}'>
                    <div class='widget-label'>{label}</div>
                    <div class='widget-value'>{value}</div>
                    <div class='widget-note'>{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-title'>Quick Action Hub</div>", unsafe_allow_html=True)
    action_labels = ['Add Project', 'Add Material', 'Process Payroll', 'View Reports']
    action_icons = ['🏗', '📦', '💸', '📊']
    action_routes = ['Project Overview', 'Materials', 'Payroll Operations', 'Reports']
    quick_cols = st.columns(4)
    for idx, col in enumerate(quick_cols):
        with col:
            if st.button(f"{action_icons[idx]} {action_labels[idx]}", key=f'action_tile_{idx}', use_container_width=True):
                navigate(action_routes[idx])

    st.caption('Ailyn House Project Control System')

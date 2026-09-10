import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style='padding: 8px 10px 18px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 18px;'>
                <div style='display:flex; align-items:center; justify-content:space-between;'>
                    <div style='display:flex; align-items:center; gap:10px;'>
                        <div style='width:34px;height:34px;border-radius:12px;background:linear-gradient(135deg, rgba(0,255,153,0.18), rgba(0,255,153,0.04)); border:1px solid rgba(0,255,153,0.35); display:flex;align-items:center;justify-content:center;color:#00ff99;font-size:1.2rem;font-weight:900;'>A</div>
                        <div style='font-size:0.72rem; letter-spacing:0.18em; color:#b6f5d9; opacity:0.9; text-transform:uppercase;'>Control</div>
                    </div>
                    <div style='width:10px; height:10px; border-radius:50%; background:#00ff99; box-shadow:0 0 14px rgba(0,255,153,0.9);'></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='text-align:center; padding: 12px 8px 18px;'>
                <div style='display:flex;justify-content:center;align-items:center; margin-bottom:14px;'>
                    <div style='width:62px; height:62px; border-radius:20px; background:linear-gradient(135deg, rgba(0,255,153,0.23), rgba(0,255,153,0.06)); border:1px solid rgba(0,255,153,0.4); display:flex;align-items:center;justify-content:center; color:#00ff99; font-size:2rem; font-weight:900; box-shadow:0 0 28px rgba(0,255,153,0.12);'>A</div>
                </div>
                <div style='font-size: 1.9rem; font-weight: 900; letter-spacing: 0.06em; line-height:1.08; color:white;'>AILY HOUSE</div>
                <div style='font-size: 0.7rem; letter-spacing: 0.22em; opacity:0.8; margin-top: 7px; color: #dffef3; text-transform:uppercase;'>Official Project</div>
                <div style='font-size: 0.7rem; letter-spacing: 0.22em; opacity:0.9; margin-top: 4px; color: #dffef3; text-transform:uppercase;'>Control System</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        now = datetime.now(ZoneInfo('Asia/Manila'))
        st.markdown(
            f"""
            <div style='padding: 8px 8px 14px; margin-top: 2px;'>
                <div style='border:1px solid rgba(0,255,153,0.2); border-radius:16px; padding:12px 12px; background:linear-gradient(135deg, rgba(0,255,153,0.06), rgba(0,255,153,0.02)); box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);'>
                    <div style='display:flex; align-items:center; gap:8px; color:#7ef5c2; font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;'><span style='width:8px;height:8px;border-radius:50%;background:#00ff99;display:inline-block;box-shadow:0 0 12px rgba(0,255,153,0.9);'></span> Live System</div>
                    <div style='margin-top:8px; color:#eefcf8; font-size:0.92rem; font-weight:700;'>{now.strftime('%I:%M:%S %p')}</div>
                    <div style='margin-top:4px; color:#bfead8; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase;'>{now.strftime('%b %d, %Y')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top:14px; margin-bottom:10px; color:#d9f7eb; font-size:0.68rem; letter-spacing:0.18em; text-transform:uppercase; opacity:0.9;'>Navigation</div>", unsafe_allow_html=True)

        nav = [
            "Dashboard",
            "Project Overview",
            "Project Control",
            "Financial Operations",
            "Payroll Operations",
            "Administration",
            "Word Puzzle",
        ]
        for label in nav:
            active = label == st.session_state.get('page', 'Dashboard')
            st.markdown(
                f"""
                <div style='margin-top:10px;'>
                    <a href='?page={label.replace(" ", "%20")}' style='display:block;padding:12px 14px;border-radius:14px;border:1px solid {"rgba(0,255,153,0.2)" if active else "rgba(255,255,255,0.06)"}; background:{"linear-gradient(135deg, rgba(0,255,153,0.12), rgba(0,255,153,0.04))" if active else "rgba(255,255,255,0.02)"}; color:white; text-decoration:none; font-weight:700; letter-spacing:0.04em; box-shadow:{"inset 0 0 0 1px rgba(0,255,153,0.06), 0 0 18px rgba(0,255,153,0.08)" if active else "none"};'>
                        {label}
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='padding: 10px 0; color:#dfeae3; font-size:0.68rem; letter-spacing:0.18em; text-transform:uppercase; opacity:0.8;'>System</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style='margin-top:8px; display:block; padding:12px 14px; border-radius:14px; border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.02); color:white; text-decoration:none; font-weight:700;'>Reset System</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style='margin-top:8px; display:block; padding:12px 14px; border-radius:14px; border:1px solid rgba(255,255,255,0.06); background:rgba(255,255,255,0.02); color:white; text-decoration:none; font-weight:700;'>Project Details</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='margin-top: 28px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08); color:rgba(255,255,255,0.68); font-size:0.76rem; text-align:center; letter-spacing:0.08em; text-transform:uppercase;'>
                AILY House Project Control System v1.0
            </div>
            """,
            unsafe_allow_html=True,
        )

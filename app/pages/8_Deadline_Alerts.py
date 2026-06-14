from __future__ import annotations

import streamlit as st

import auth
from db import get_deadline_alerts, get_expired_jobs
from utils import render_section_title


st.set_page_config(
    page_title="Deadline Alerts",
    page_icon="⏰",
    layout="wide",
)


def display_upcoming_deadlines() -> None:
    st.subheader("Closing Within 7 Days")

    upcoming_jobs = get_deadline_alerts(days=7)

    if upcoming_jobs.empty:
        st.info("No opportunities are scheduled to close within the next 7 days.")
    else:
        st.dataframe(
            upcoming_jobs,
            use_container_width=True,
            hide_index=True,
        )


def display_expired_opportunities() -> None:
    st.subheader("Expired Jobs")

    expired_jobs = get_expired_jobs()

    if expired_jobs.empty:
        st.info("No expired opportunities found.")
    else:
        st.dataframe(
            expired_jobs,
            use_container_width=True,
            hide_index=True,
        )


def load_dashboard() -> None:
    auth.init_session_state()
    auth.render_login_panel()

    st.title("Deadline Alerts")

    render_section_title(
        "Upcoming and Expired Opportunities",
        "Track opportunities nearing their deadline and those already expired.",
    )

    col1, col2 = st.columns(2)

    with col1:
        display_upcoming_deadlines()

    with col2:
        display_expired_opportunities()


if __name__ == "__main__":
    load_dashboard()

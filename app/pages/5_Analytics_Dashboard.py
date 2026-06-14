from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

import auth
from db import get_opportunities
from utils import (
    deadline_bucket_frame,
    render_section_title,
    top_skills_frame,
)

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📈",
    layout="wide",
)


def calculate_statistics(data: pd.DataFrame) -> dict:
    if data.empty:
        return {
            "total": 0,
            "open": 0,
            "closed": 0,
            "remote": 0,
            "hybrid": 0,
            "companies": 0,
        }

    status_series = data["status"].astype(str).str.lower()
    mode_series = data["work_mode"].astype(str).str.lower()

    return {
        "total": len(data),
        "open": int((status_series == "open").sum()),
        "closed": int(
            status_series.isin(
                ["closed", "expired", "archived"]
            ).sum()
        ),
        "remote": int((mode_series == "remote").sum()),
        "hybrid": int((mode_series == "hybrid").sum()),
        "companies": int(data["company_name"].nunique()),
    }


def prepare_chart_data(data: pd.DataFrame):
    categories = (
        data["category"]
        .value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "category"})
    )

    work_modes = (
        data["work_mode"]
        .value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "work_mode"})
    )

    statuses = (
        data["status"]
        .value_counts()
        .reset_index(name="count")
        .rename(columns={"index": "status"})
    )

    salary_data = data.copy()
    salary_data["average_salary"] = (
        salary_data["salary_min"].astype(float)
        + salary_data["salary_max"].astype(float)
    ) / 2

    return (
        categories,
        work_modes,
        statuses,
        salary_data,
        top_skills_frame(data),
        deadline_bucket_frame(data),
    )


def display_kpis(metrics: dict) -> None:
    columns = st.columns(6)

    columns[0].metric("Total Opportunities", metrics["total"])
    columns[1].metric("Open Jobs", metrics["open"])
    columns[2].metric("Closed Jobs", metrics["closed"])
    columns[3].metric("Remote Jobs", metrics["remote"])
    columns[4].metric("Hybrid Jobs", metrics["hybrid"])
    columns[5].metric("Total Companies", metrics["companies"])


def build_dashboard() -> None:
    auth.init_session_state()
    auth.render_login_panel()

    st.title("Analytics Dashboard")
    render_section_title(
        "Operational Insights",
        "A quick snapshot of the opportunity dataset.",
    )

    try:
        opportunities = get_opportunities(
            limit=5000,
            sort_by="created_at",
            sort_order="DESC",
        )
    except Exception as err:
        st.error(f"Unable to load analytics data: {err}")
        return

    stats = calculate_statistics(opportunities)
    display_kpis(stats)

    if opportunities.empty:
        st.info("No analytics data found.")
        return

    (
        category_df,
        workmode_df,
        status_df,
        salary_df,
        skills_df,
        deadline_df,
    ) = prepare_chart_data(opportunities)

    left_col, right_col = st.columns(2)

    with left_col:
        category_chart = px.bar(
            category_df,
            x="category",
            y="count",
            color="category",
            title="Category Distribution",
        )
        st.plotly_chart(category_chart, use_container_width=True)

    with right_col:
        workmode_chart = px.pie(
            workmode_df,
            names="work_mode",
            values="count",
            hole=0.35,
            title="Work Mode Distribution",
        )
        st.plotly_chart(workmode_chart, use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        status_chart = px.bar(
            status_df,
            x="status",
            y="count",
            color="status",
            title="Status Distribution",
        )
        st.plotly_chart(status_chart, use_container_width=True)

    with right_col:
        salary_chart = px.box(
            salary_df,
            x="category",
            y="average_salary",
            title="Salary Analysis",
            points="all",
        )
        st.plotly_chart(salary_chart, use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        if skills_df.empty:
            st.info("No skills data available.")
        else:
            skills_chart = px.bar(
                skills_df,
                x="skill",
                y="count",
                color="count",
                title="Top Skills Analysis",
            )
            st.plotly_chart(skills_chart, use_container_width=True)

    with right_col:
        if deadline_df.empty:
            st.info("No deadline trend data available.")
        else:
            deadline_chart = px.line(
                deadline_df,
                x="deadline",
                y="count",
                markers=True,
                title="Deadline Trends",
            )
            st.plotly_chart(deadline_chart, use_container_width=True)


if __name__ == "__main__":
    build_dashboard()

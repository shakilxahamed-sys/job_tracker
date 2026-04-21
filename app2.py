import streamlit as st
import pandas as pd
import plotly.express as px
from database2 import load_data, save_data, add_job, update_status, delete_job
from datetime import date

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Job Tracker",
    page_icon="💼",
    layout="wide"
)

# ── CUSTOM CSS ──
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton>button {
        background-color: #1A5276;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ── SIDEBAR NAVIGATION ──
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
st.sidebar.title("💼 Job Tracker")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "➕ Add Job", "✏️ Update Status", "🗑️ Delete Job"]
)

# ── LOAD DATA ──
df = load_data()

# ════════════════════════════════
# 🏠 PAGE 1 — DASHBOARD
# ════════════════════════════════
if page == "🏠 Dashboard":
    st.title("🏠 Job Application Dashboard")
    st.markdown("Track all your job applications in one place!")
    st.markdown("---")

    # Stats row
    if len(df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📋 Total Applied", len(df))
        col2.metric("🎯 Interviews", len(df[df["Status"] == "Interview"]))
        col3.metric("✅ Offers", len(df[df["Status"] == "Offered"]))
        col4.metric("❌ Rejected", len(df[df["Status"] == "Rejected"]))

        st.markdown("---")

        # Chart
        st.subheader("📊 Applications by Status")
        status_count = df["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        fig = px.pie(
            status_count,
            names="Status",
            values="Count",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Filter
        st.subheader("📋 All Applications")
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Applied", "Interview", "Offered", "Rejected"]
        )
        if filter_status == "All":
            st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(
                df[df["Status"] == filter_status],
                use_container_width=True
            )
    else:
        st.info("No job applications yet! Go to ➕ Add Job to get started!")

# ════════════════════════════════
# ➕ PAGE 2 — ADD JOB
# ════════════════════════════════
elif page == "➕ Add Job":
    st.title("➕ Add New Job Application")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("🏢 Company Name")
        role = st.text_input("💼 Job Role")
        date_applied = st.date_input("📅 Date Applied", value=date.today())

    with col2:
        status = st.selectbox(
            "📌 Status",
            ["Applied", "Interview", "Offered", "Rejected"]
        )
        notes = st.text_area("📝 Notes", placeholder="Any notes about this job...")

    st.markdown("---")

    if st.button("➕ Add Job Application"):
        if company and role:
            add_job(company, role, str(date_applied), status, notes)
            st.success(f"✅ Successfully added {role} at {company}!")
            st.balloons()
        else:
            st.error("❌ Please enter Company Name and Role!")

# ════════════════════════════════
# ✏️ PAGE 3 — UPDATE STATUS
# ════════════════════════════════
elif page == "✏️ Update Status":
    st.title("✏️ Update Job Status")
    st.markdown("---")

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            index = st.number_input(
                "Enter Row Number to Update",
                min_value=0,
                max_value=len(df)-1,
                step=1
            )
        with col2:
            new_status = st.selectbox(
                "New Status",
                ["Applied", "Interview", "Offered", "Rejected"]
            )

        if st.button("✏️ Update Status"):
            update_status(index, new_status)
            st.success(f"✅ Status updated to {new_status}!")
            st.rerun()
    else:
        st.info("No jobs added yet!")

# ════════════════════════════════
# 🗑️ PAGE 4 — DELETE JOB
# ════════════════════════════════
elif page == "🗑️ Delete Job":
    st.title("🗑️ Delete Job Application")
    st.markdown("---")

    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")

        index = st.number_input(
            "Enter Row Number to Delete",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button("🗑️ Delete Job"):
            delete_job(index)
            st.success("✅ Job deleted successfully!")
            st.rerun()
    else:
        st.info("No jobs to delete!")

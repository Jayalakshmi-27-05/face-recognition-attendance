import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AI Attendance Dashboard", layout="wide")

st.title("📊 AI Face Recognition Attendance Dashboard")

# -----------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------
if not os.path.exists("attendance.csv"):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv("attendance.csv", index=False)

# Load attendance
df = pd.read_csv("attendance.csv")

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Unique Students", df["Name"].nunique())

with col3:
    st.metric("Days Recorded", df["Date"].nunique())

st.markdown("---")

# -----------------------------
# BAR CHART
# -----------------------------
st.subheader("📊 Attendance Count")

if not df.empty:
    st.bar_chart(df["Name"].value_counts())

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📋 Attendance Records")
st.dataframe(df, use_container_width=True)

# -----------------------------
# FILTER
# -----------------------------
if not df.empty:

    st.subheader("🔍 Filter by Student")

    name = st.selectbox(
        "Select Student",
        df["Name"].unique()
    )

    filtered = df[df["Name"] == name]

    st.dataframe(filtered, use_container_width=True)

else:
    st.warning("No attendance data yet")

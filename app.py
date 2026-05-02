import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Attendance Dashboard", layout="wide")

st.title("📊 AI Face Recognition Attendance System")

# Load data
df = pd.read_csv("attendance.csv")

# ---------------------------
# 🧾 TOP CARDS (METRICS)
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 👥 Total Records")
    st.metric("Count", len(df))

with col2:
    st.markdown("### 🧑‍🎓 Unique Students")
    st.metric("Students", df["Name"].nunique())

with col3:
    st.markdown("### 📅 Days Recorded")
    st.metric("Days", df["Date"].nunique())

st.markdown("---")

# ---------------------------
# 📊 BAR CHART
# ---------------------------
st.subheader("📊 Attendance Count per Student")
count_data = df["Name"].value_counts()
st.bar_chart(count_data)

# ---------------------------
# 📈 DAILY ATTENDANCE
# ---------------------------
st.subheader("📅 Daily Attendance Trend")
daily = df.groupby("Date").count()["Name"]
st.line_chart(daily)

st.markdown("---")

# ---------------------------
# 📋 FULL TABLE
# ---------------------------
st.subheader("📋 Attendance Records")
st.dataframe(df, use_container_width=True)

# ---------------------------
# 🔍 FILTER SECTION
# ---------------------------
st.subheader("🔍 Filter Data")

name = st.selectbox("Select Student", df["Name"].unique())
filtered = df[df["Name"] == name]

st.write("Filtered Records:")
st.dataframe(filtered, use_container_width=True)

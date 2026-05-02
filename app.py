```python
import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(
    page_title="AI Attendance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #00FFAA;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #00FFAA;
    }
    to {
        text-shadow: 0 0 20px #00FFAA,
                     0 0 40px #00FFAA;
    }
}

.metric-card {
    background: linear-gradient(145deg, #1e1e1e, #252525);
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0px 0px 15px rgba(0,255,170,0.3);
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: scale(1.05);
}

.section-title {
    color: #00FFAA;
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# TITLE
# ---------------------------------
st.markdown(
    '<p class="main-title">🤖 AI Face Recognition Attendance Dashboard</p>',
    unsafe_allow_html=True
)

# ---------------------------------
# AUTO REFRESH
# ---------------------------------
refresh = st.sidebar.slider(
    "Refresh every (seconds)",
    5,
    60,
    10
)

# ---------------------------------
# CREATE FILE IF NOT EXISTS
# ---------------------------------
if not os.path.exists("attendance.csv"):
    df = pd.DataFrame(columns=["Name", "Date", "Time"])
    df.to_csv("attendance.csv", index=False)

# ---------------------------------
# LOAD DATA
# ---------------------------------
try:
    df = pd.read_csv("attendance.csv")
except:
    df = pd.DataFrame(columns=["Name", "Date", "Time"])

# ---------------------------------
# METRIC CARDS
# ---------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h2>👥 Total Records</h2>
        <h1>{len(df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h2>🧑‍🎓 Unique Students</h2>
        <h1>{df['Name'].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h2>📅 Attendance Days</h2>
        <h1>{df['Date'].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# CHARTS
# ---------------------------------
if not df.empty:

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<p class="section-title">📊 Attendance Count</p>',
            unsafe_allow_html=True
        )

        attendance_count = df["Name"].value_counts()
        st.bar_chart(attendance_count)

    with right:
        st.markdown(
            '<p class="section-title">📈 Daily Attendance Trend</p>',
            unsafe_allow_html=True
        )

        daily = df.groupby("Date").count()["Name"]
        st.line_chart(daily)

st.markdown("---")

# ---------------------------------
# FILTER SECTION
# ---------------------------------
st.markdown(
    '<p class="section-title">🔍 Filter Records</p>',
    unsafe_allow_html=True
)

if not df.empty:

    selected_name = st.selectbox(
        "Select Student",
        ["All"] + list(df["Name"].unique())
    )

    if selected_name == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Name"] == selected_name]

    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("No attendance records available")

# ---------------------------------
# SIDEBAR STATUS
# ---------------------------------
st.sidebar.success("🟢 System Active")
st.sidebar.info("🤖 AI Attendance Monitoring Running")

# ---------------------------------
# AUTO REFRESH
# ---------------------------------
time.sleep(refresh)
st.rerun()
```


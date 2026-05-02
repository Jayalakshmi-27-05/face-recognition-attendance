import streamlit as st
        <h1>{df['Date'].nunique()}</h1>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# CHARTS SECTION
# ---------------------------------
if not df.empty:

    left, right = st.columns(2)

    with left:
        st.markdown('<p class="section-title">📊 Attendance Count</p>', unsafe_allow_html=True)
        attendance_count = df["Name"].value_counts()
        st.bar_chart(attendance_count)

    with right:
        st.markdown('<p class="section-title">📈 Daily Attendance Trend</p>', unsafe_allow_html=True)
        daily = df.groupby("Date").count()["Name"]
        st.line_chart(daily)

st.markdown("---")

# ---------------------------------
# FILTER SECTION
# ---------------------------------
st.markdown('<p class="section-title">🔍 Filter Records</p>', unsafe_allow_html=True)

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
# LIVE STATUS
# ---------------------------------
st.sidebar.success("🟢 System Active")
st.sidebar.info("🤖 AI Attendance Monitoring Running")

# ---------------------------------
# AUTO REFRESH TIMER
# ---------------------------------
time.sleep(refresh)
st.rerun()

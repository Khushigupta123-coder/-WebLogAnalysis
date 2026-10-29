import streamlit as st

st.title("📈 Traffic Trends")
st.caption("Explore requests over time. Timestamps are converted to UTC for consistent grouping.")
df = st.session_state["web_log_df"].copy()
valid = df[df["TimestampParsed"].notna()].copy()

if valid.empty:
    st.warning("No timestamps could be parsed from this dataset, so traffic-over-time charts are unavailable.")
    st.dataframe(df[["IP", "Timestamp", "Page", "Status"]].head(20), use_container_width=True, hide_index=True)
    st.stop()

c1, c2 = st.columns(2)
c1.metric("Records with usable timestamps", f"{len(valid):,}")
c2.metric("Distinct UTC dates", f"{valid['TimestampParsed'].dt.date.nunique():,}")

hourly = valid.set_index("TimestampParsed").resample("h").size().rename("Requests")
daily = valid.set_index("TimestampParsed").resample("D").size().rename("Requests")
left, right = st.columns(2, gap="large")
with left:
    st.subheader("Requests by hour")
    st.line_chart(hourly, x_label="Time (UTC)", y_label="Requests", use_container_width=True)
with right:
    st.subheader("Requests by day")
    st.bar_chart(daily, x_label="Date (UTC)", y_label="Requests", use_container_width=True)

st.subheader("Traffic by request method")
method_counts = valid["Method"].value_counts().rename_axis("Method").reset_index(name="Requests")
st.bar_chart(method_counts.set_index("Method"), use_container_width=True)

st.subheader("Peak hour")
if not hourly.empty:
    peak_time = hourly.idxmax()
    peak_count = int(hourly.max())
    st.info(f"Highest observed hour: **{peak_time.strftime('%Y-%m-%d %H:%M UTC')}** with **{peak_count:,} requests**. This reflects the uploaded/sample dataset only.")

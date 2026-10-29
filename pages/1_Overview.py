import streamlit as st

from backend.analytics import clean_display_df, format_bytes

st.markdown(
    "<div class='hero'><div class='hero-kicker'>Analytics command center</div>"
    "<div class='hero-title'>Web log overview</div>"
    "<p class='hero-sub'>A quick health check of requests, traffic, errors and data quality.</p></div>",
    unsafe_allow_html=True,
)

df = st.session_state["web_log_df"]
source = st.session_state["web_log_source"]
stats = st.session_state["web_log_stats"]
top_n = st.session_state.get("top_n", 10)

total_requests = len(df)
unique_ips = int(df["IP"].nunique())
error_count = int((df["Status"] >= 400).sum())
error_rate = (error_count / total_requests * 100) if total_requests else 0
bytes_total = int(df["Bytes"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total requests", f"{total_requests:,}")
c2.metric("Unique IP addresses", f"{unique_ips:,}")
c3.metric("HTTP errors", f"{error_count:,}", f"{error_rate:.1f}% of requests", delta_color="inverse")
c4.metric("Data transferred", format_bytes(bytes_total))

st.caption(f"**Dataset:** {source} · **Parsing quality:** {stats['parsed_lines']:,} valid / {stats['nonempty_lines']:,} non-empty lines · **Rejected:** {stats['rejected_lines']:,}")

left, right = st.columns(2, gap="large")
with left:
    st.subheader("HTTP status distribution")
    status_counts = df["Status"].value_counts().sort_index()
    st.bar_chart(status_counts, x_label="HTTP status code", y_label="Requests", use_container_width=True)
with right:
    st.subheader("Most requested endpoints")
    page_counts = df["Page"].value_counts().head(top_n)
    st.bar_chart(page_counts.sort_values(), x_label="Endpoint", y_label="Requests", horizontal=True, use_container_width=True)

st.subheader("Quick observations")
insights = []
if not df.empty:
    top_page = df["Page"].value_counts().idxmax()
    top_page_count = int(df["Page"].value_counts().max())
    insights.append(f"The most requested endpoint is **`{top_page}`** with **{top_page_count:,} requests**.")
    top_method = df["Method"].value_counts().idxmax()
    insights.append(f"The most common request method is **{top_method}**.")
    if error_count:
        insights.append(f"There are **{error_count:,} error responses** (HTTP 4xx/5xx), equal to **{error_rate:.1f}%** of parsed requests.")
    else:
        insights.append("No HTTP 4xx/5xx responses were found in this dataset.")
    if stats["rejected_lines"]:
        insights.append(f"**{stats['rejected_lines']:,} lines** could not be parsed. Check the source format or inspect the uploaded file.")
for item in insights:
    st.markdown(f"- {item}")

st.subheader("Latest parsed records")
st.dataframe(clean_display_df(df).head(12), use_container_width=True, hide_index=True)

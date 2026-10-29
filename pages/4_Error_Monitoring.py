import streamlit as st

from backend.analytics import clean_display_df

st.title("🚦 Error Monitoring")
st.caption("Review HTTP client errors (4xx), server errors (5xx), and the endpoints where they occur.")
df = st.session_state["web_log_df"].copy()
errors = df[df["Status"] >= 400].copy()
client_errors = int(((df["Status"] >= 400) & (df["Status"] < 500)).sum())
server_errors = int((df["Status"] >= 500).sum())
total = len(df)
rate = len(errors) / total * 100 if total else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total errors", f"{len(errors):,}", f"{rate:.1f}% of requests", delta_color="inverse")
c2.metric("Client errors (4xx)", f"{client_errors:,}")
c3.metric("Server errors (5xx)", f"{server_errors:,}")

left, right = st.columns(2, gap="large")
with left:
    st.subheader("Errors by status code")
    if errors.empty:
        st.success("No 4xx/5xx responses found in this dataset.")
    else:
        st.bar_chart(errors["Status"].value_counts().sort_index(), x_label="Status", y_label="Errors", use_container_width=True)
with right:
    st.subheader("Endpoints returning errors")
    if errors.empty:
        st.write("There are no error endpoints to display.")
    else:
        endpoint_errors = errors["Page"].value_counts().head(10).sort_values()
        st.bar_chart(endpoint_errors, x_label="Errors", y_label="Endpoint", horizontal=True, use_container_width=True)

st.subheader("Error records")
if errors.empty:
    st.info("Try another access log file if you want to inspect error responses.")
else:
    st.dataframe(clean_display_df(errors), use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download error records CSV", errors.drop(columns=["TimestampParsed"], errors="ignore").to_csv(index=False).encode("utf-8"), "web_log_errors.csv", "text/csv")

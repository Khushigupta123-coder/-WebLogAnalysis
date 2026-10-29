from datetime import datetime
import streamlit as st

from backend.analytics import clean_display_df, format_bytes, map_reduce

st.title("📥 Reports & Export")
st.caption("Download the parsed dataset, error records, or MapReduce-style summary tables.")
df = st.session_state["web_log_df"].copy()
source = st.session_state["web_log_source"]
stats = st.session_state["web_log_stats"]
errors = df[df["Status"] >= 400].copy()

summary_text = f"""WEB LOG ANALYSIS REPORT
Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}
Source: {source}

DATASET SUMMARY
Total valid requests: {len(df):,}
Unique IP addresses: {df['IP'].nunique():,}
HTTP errors (4xx/5xx): {len(errors):,}
Error rate: {(len(errors) / len(df) * 100) if len(df) else 0:.2f}%
Bytes transferred: {int(df['Bytes'].sum()):,} ({format_bytes(int(df['Bytes'].sum()))})
Non-empty source lines: {stats['nonempty_lines']:,}
Parsed lines: {stats['parsed_lines']:,}
Rejected lines: {stats['rejected_lines']:,}

SCOPE NOTE
MapReduce-style aggregation is performed locally in Python. This app does not run a Hadoop cluster.
"""

c1, c2, c3 = st.columns(3)
c1.metric("Rows ready to export", f"{len(df):,}")
c2.metric("Error rows", f"{len(errors):,}")
c3.metric("Data transferred", format_bytes(int(df["Bytes"].sum())))

st.download_button("⬇️ Download project summary (.txt)", summary_text, "web_log_analysis_report.txt", "text/plain", use_container_width=True)
st.download_button("⬇️ Download all parsed records (.csv)", clean_display_df(df).to_csv(index=False).encode("utf-8"), "parsed_web_logs.csv", "text/csv", use_container_width=True)
st.download_button("⬇️ Download error records (.csv)", clean_display_df(errors).to_csv(index=False).encode("utf-8"), "web_log_errors.csv", "text/csv", use_container_width=True)

key = st.selectbox("Create a summary grouped by", ["Page", "Status", "IP", "Method", "Status Group"])
summary = map_reduce(df.to_dict("records"), key)
st.dataframe(summary.head(20), use_container_width=True, hide_index=True)
st.download_button("⬇️ Download grouped summary (.csv)", summary.to_csv(index=False).encode("utf-8"), f"summary_by_{key.lower().replace(' ', '_')}.csv", "text/csv")

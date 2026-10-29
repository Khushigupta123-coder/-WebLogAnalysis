import streamlit as st

from backend.analytics import clean_display_df

st.title("🔎 Log Explorer")
st.caption("Search and filter parsed records. Downloads follow the filters you select.")
df = st.session_state["web_log_df"].copy()
top_n = st.session_state.get("top_n", 10)

with st.container(border=True):
    search = st.text_input("Search IP, endpoint, method or status", placeholder="e.g. 192.168.1.10 or /login")
    c1, c2, c3 = st.columns(3)
    methods = sorted(df["Method"].dropna().astype(str).unique().tolist())
    statuses = sorted(df["Status"].dropna().astype(int).unique().tolist())
    groups = sorted(df["Status Group"].dropna().astype(str).unique().tolist())
    selected_methods = c1.multiselect("Request method", methods, default=methods)
    selected_statuses = c2.multiselect("HTTP status", statuses)
    selected_groups = c3.multiselect("Status class", groups)

filtered = df.copy()
if search.strip():
    needle = search.strip().lower()
    searchable = filtered[["IP", "Page", "Method", "Status", "Timestamp"]].astype(str).agg(" ".join, axis=1).str.lower()
    filtered = filtered[searchable.str.contains(needle, regex=False)]
if selected_methods:
    filtered = filtered[filtered["Method"].astype(str).isin(selected_methods)]
else:
    filtered = filtered.iloc[0:0]
if selected_statuses:
    filtered = filtered[filtered["Status"].isin(selected_statuses)]
if selected_groups:
    filtered = filtered[filtered["Status Group"].isin(selected_groups)]

m1, m2 = st.columns(2)
m1.metric("Matching records", f"{len(filtered):,}")
m2.metric("Unique IPs in results", f"{filtered['IP'].nunique():,}")
st.dataframe(clean_display_df(filtered), use_container_width=True, hide_index=True, height=460)
st.download_button(
    "⬇️ Download filtered records as CSV",
    data=clean_display_df(filtered).to_csv(index=False).encode("utf-8"),
    file_name="filtered_web_logs.csv",
    mime="text/csv",
    use_container_width=False,
)
st.caption(f"The sidebar's Top results setting is currently {top_n}; all matching rows are shown in this explorer.")

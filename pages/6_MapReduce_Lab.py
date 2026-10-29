import streamlit as st

from backend.analytics import map_reduce

st.title("⚙️ MapReduce Lab")
st.caption("Explore the Map → Shuffle/Group → Reduce idea using the parsed access-log records.")
df = st.session_state["web_log_df"].copy()
top_n = st.session_state.get("top_n", 10)
key = st.selectbox("Choose the field to aggregate", ["Page", "Status", "IP", "Method", "Status Group"], index=0)

mapper, shuffle, reducer = st.columns(3, gap="medium")
with mapper:
    st.markdown("#### 1 · Map")
    st.write("Emit each selected key with the value `1`.")
    mapped = df[[key]].copy()
    mapped["Value"] = 1
    st.metric("Key-value pairs", f"{len(mapped):,}")
with shuffle:
    st.markdown("#### 2 · Group")
    st.write("Group matching keys together before counting.")
    st.metric("Distinct keys", f"{df[key].nunique():,}")
with reducer:
    st.markdown("#### 3 · Reduce")
    st.write("Add the values for each key to get request counts.")
    results = map_reduce(df.to_dict("records"), key)
    st.metric("Reduced groups", f"{len(results):,}")

left, right = st.columns(2, gap="large")
with left:
    st.subheader("Mapper output sample")
    st.dataframe(mapped.head(30), use_container_width=True, hide_index=True)
with right:
    st.subheader("Reducer output")
    st.dataframe(results.head(top_n), use_container_width=True, hide_index=True)
    st.bar_chart(results.head(top_n).set_index(key)["Requests"], x_label=key, y_label="Request count", use_container_width=True)

st.download_button("⬇️ Download complete reducer output CSV", results.to_csv(index=False).encode("utf-8"), "mapreduce_results.csv", "text/csv")
st.info("Academic scope: the mapper/reducer stages are simulated in local Python. The app does not launch Hadoop or perform distributed computation across a cluster.")

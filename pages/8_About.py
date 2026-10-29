import streamlit as st

st.title("ℹ️ About WebLog Analytics")
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">Big Data Analytics mini project</div>
      <div class="hero-title">Web server log analysis</div>
      <p class="hero-sub">Turn raw Apache/Nginx access logs into readable traffic, error, and request summaries.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Project objective")
st.write("Parse web server access logs, organize valid records, summarize requests, and provide visual insights that help a user understand traffic patterns and HTTP errors.")

st.subheader("Processing pipeline")
cols = st.columns(4)
for col, title, detail in zip(
    cols,
    ["1 · Raw logs", "2 · Parse", "3 · Aggregate", "4 · Visualize"],
    ["Read the access-log text", "Extract IP, time, method, endpoint, status and bytes", "Count repeated keys using local Python logic", "Show metrics, charts, filters and exports"],
):
    with col:
        st.markdown(f"**{title}**")
        st.write(detail)

st.subheader("Technologies")
st.write("Python · Streamlit · Pandas · regular expressions · Counter-based MapReduce-style aggregation")

st.subheader("Important technical scope")
st.info("The current implementation demonstrates MapReduce concepts locally. It does not start an Apache Hadoop cluster or run distributed jobs. Describe it accurately in your report and viva.")
st.markdown("**Supported log format:** Apache/Nginx access logs in a common/combined format, for example:")
st.code('192.168.1.10 - - [28/Oct/2026:10:20:30 +0530] "GET /home HTTP/1.1" 200 1234', language="text")
st.markdown("**Data quality:** lines that do not match the parser are counted as rejected; byte sizes of `-` are treated as zero.")

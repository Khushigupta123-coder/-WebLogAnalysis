
from pathlib import Path
from collections import Counter
import re

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Project folder and default log file
ROOT = Path(__file__).parent
DEFAULT_LOG = ROOT / "data" / "access.log"


# Page settings
st.set_page_config(
    page_title="Web Log Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Web Log Analysis Dashboard")
st.caption("Big Data Mini Project | Web Server Log Analysis")

st.info(
    "This project analyses web server logs and demonstrates "
    "MapReduce-style aggregation locally. It does not run a Hadoop cluster."
)


# Parse one web server log line
def parse_line(line):
    """Extract useful information from an Apache/Nginx access log line."""

    pattern = (
        r'^(?P<ip>\S+) \S+ \S+ '
        r'\[(?P<time>[^\]]+)\] '
        r'"(?P<request>[^"]*)" '
        r'(?P<status>\d{3}) (?P<size>\S+)'
    )

    match = re.match(pattern, line.strip())

    if not match:
        return None

    request_parts = match.group("request").split()

    method = request_parts[0] if len(request_parts) >= 1 else "UNKNOWN"
    page = request_parts[1] if len(request_parts) >= 2 else "/"

    size_text = match.group("size")
    size = int(size_text) if size_text.isdigit() else 0

    return {
        "IP": match.group("ip"),
        "Timestamp": match.group("time"),
        "Method": method,
        "Page": page,
        "Status": int(match.group("status")),
        "Bytes": size
    }


# MapReduce-style aggregation
def map_reduce(records, key):
    """Count how many times each value occurs."""

    mapped = [(str(row[key]), 1) for row in records]

    counts = Counter()

    for item, value in mapped:
        counts[item] += value

    results = [
        {key: item, "Requests": count}
        for item, count in counts.most_common()
    ]

    return pd.DataFrame(results, columns=[key, "Requests"])


# Sidebar controls
with st.sidebar:
    st.header("Data Settings")

    uploaded = st.file_uploader(
        "Upload an access log file",
        type=["log", "txt"]
    )

    top_n = st.slider(
        "Number of top results",
        min_value=5,
        max_value=20,
        value=10
    )

    st.caption("Expected format: Apache/Nginx access logs.")


# Load uploaded file or included sample file
try:
    if uploaded is not None:
        raw_text = uploaded.getvalue().decode(
            "utf-8",
            errors="replace"
        )
        source_label = uploaded.name

    else:
        if not DEFAULT_LOG.exists():
            st.error(
                "Sample log file not found. Please check that "
                "data/access.log exists inside the project folder."
            )
            st.stop()

        raw_text = DEFAULT_LOG.read_text(
            encoding="utf-8",
            errors="replace"
        )
        source_label = "Included sample access.log"

except OSError as error:
    st.error(f"Could not read the log file: {error}")
    st.stop()


# Parse the log data
lines = [line for line in raw_text.splitlines() if line.strip()]

parsed = []

for line in lines:
    record = parse_line(line)

    if record is not None:
        parsed.append(record)

df = pd.DataFrame(parsed)


# Check whether any valid records were found
if df.empty:
    st.error(
        "No valid log lines found. Please upload an Apache/Nginx "
        "access log file in the expected format."
    )
    st.stop()


# Calculate summary statistics
df["Status Group"] = df["Status"].apply(
    lambda status: f"{status // 100}xx"
)

total_requests = len(df)
unique_ips = df["IP"].nunique()
error_requests = int((df["Status"] >= 400).sum())
total_bytes = int(df["Bytes"].sum())


# Display summary cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Valid Requests", f"{total_requests:,}")
col2.metric("Unique IP Addresses", f"{unique_ips:,}")
col3.metric("Errors (4xx/5xx)", f"{error_requests:,}")
col4.metric("Data Transferred", f"{total_bytes:,} bytes")

st.caption(
    f"Source: {source_label} | "
    f"Parsed {total_requests} of {len(lines)} non-empty lines"
)


# Dashboard tabs
overview, details, raw, about = st.tabs(
    ["Overview", "MapReduce Results", "Parsed Records", "About Project"]
)


# TAB 1: Overview
with overview:
    left, right = st.columns(2)

    with left:
        st.subheader("HTTP Status Codes")

        status_counts = df["Status"].value_counts().sort_index()

        fig, ax = plt.subplots()
        ax.bar(status_counts.index.astype(str), status_counts.values)
        ax.set_xlabel("HTTP Status Code")
        ax.set_ylabel("Number of Requests")
        ax.set_title("Requests by Status Code")

        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.subheader("Most Requested Pages")

        pages = df["Page"].value_counts().head(top_n).sort_values()

        fig, ax = plt.subplots()
        ax.barh(pages.index, pages.values)
        ax.set_xlabel("Number of Requests")
        ax.set_ylabel("Page")
        ax.set_title("Top Requested Pages")

        st.pyplot(fig)
        plt.close(fig)

    st.subheader("HTTP Method Breakdown")

    methods = (
        df["Method"]
        .value_counts()
        .rename_axis("Method")
        .reset_index(name="Requests")
    )

    st.dataframe(methods, use_container_width=True)


# TAB 2: MapReduce Results
with details:
    st.subheader("MapReduce-Style Aggregations")

    st.write(
        "Mapper: emits a key and the value 1 for each request. "
        "Reducer: adds values for matching keys."
    )

    key_label = st.selectbox(
        "Choose a category to analyse",
        ["Page", "Status", "IP", "Method", "Status Group"]
    )

    result = map_reduce(df.to_dict("records"), key_label)

    st.dataframe(result.head(top_n), use_container_width=True)

    st.download_button(
        "Download Aggregation CSV",
        result.to_csv(index=False).encode("utf-8"),
        "mapreduce_results.csv",
        "text/csv"
    )

    st.subheader("Top Client IP Addresses")

    ip_results = map_reduce(df.to_dict("records"), "IP")

    st.dataframe(ip_results.head(top_n), use_container_width=True)


# TAB 3: Parsed Records
with raw:
    st.subheader("Parsed Access Log Records")

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Parsed Records CSV",
        df.to_csv(index=False).encode("utf-8"),
        "parsed_web_logs.csv",
        "text/csv"
    )


# TAB 4: About Project
with about:
    st.subheader("Project Summary")

    st.markdown("""
    **Objective:** Analyse web server logs to understand website traffic
    and identify HTTP errors.

    **Pipeline:** Raw log lines → Parsing → Mapper key-value pairs
    → Reducer counts → Dashboard.

    **Technologies:** Python, Pandas, Streamlit, Matplotlib and Counter.

    **Big Data Concept:** MapReduce groups records by a key and combines
    their values. This project demonstrates that concept locally.

    **Limitation:** This version does not execute Apache Hadoop.
    If actual Hadoop execution is required by your assignment, the
    project must be extended with Hadoop Streaming.
    """)

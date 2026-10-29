from pathlib import Path
import streamlit as st

from backend.analytics import parse_log_text, load_default_text, dataframe_for_app

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="WebLog Analytics | Command Center",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Shared visual theme used by every page.
st.markdown(
    """
    <style>
      .stApp { background: radial-gradient(ellipse at top left, rgba(81, 65, 160, .13), transparent 40%), #0b1020; }
      [data-testid="stSidebar"] { background: #0e1528; border-right: 1px solid rgba(148,163,184,.16); }
      [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #cbd5e1; }
      .block-container { padding-top: 1.6rem; padding-bottom: 2.4rem; max-width: 1500px; }
      h1, h2, h3 { letter-spacing: -0.025em; }
      [data-testid="stMetric"] { background: linear-gradient(145deg, rgba(30,41,73,.86), rgba(20,27,48,.86)); border: 1px solid rgba(148,163,184,.18); padding: 16px 18px; border-radius: 16px; }
      [data-testid="stMetricLabel"] { color: #a5b4fc; }
      [data-testid="stMetricValue"] { color: #f8fafc; }
      [data-testid="stDataFrame"] { border: 1px solid rgba(148,163,184,.18); border-radius: 12px; overflow: hidden; }
      div[data-testid="stAlert"] { border-radius: 12px; }
      .hero { padding: 1.2rem 1.35rem; border: 1px solid rgba(129,140,248,.28); border-radius: 18px; background: linear-gradient(115deg, rgba(49,46,129,.48), rgba(15,23,42,.5)); margin-bottom: 1rem; }
      .hero-kicker { text-transform: uppercase; letter-spacing: .16em; color: #a5b4fc; font-size: .72rem; font-weight: 700; }
      .hero-title { margin: .25rem 0 .35rem 0; font-size: 1.8rem; font-weight: 750; color: #f8fafc; }
      .hero-sub { color: #cbd5e1; margin: 0; font-size: .96rem; }
      .small-note { color: #94a3b8; font-size: .85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.navigation enables real page navigation while this entrypoint keeps the
# upload and common data available to every page.
nav = st.navigation(
    {
        "WORKSPACE": [
            st.Page("pages/1_Overview.py", title="Overview", icon="📊", default=True),
            st.Page("pages/2_Log_Explorer.py", title="Log Explorer", icon="🔎"),
            st.Page("pages/3_Traffic_Trends.py", title="Traffic Trends", icon="📈"),
        ],
        "MONITORING": [
            st.Page("pages/4_Error_Monitoring.py", title="Error Monitoring", icon="🚦"),
            st.Page("pages/5_Security_Insights.py", title="Security Insights", icon="🛡️"),
        ],
        "ANALYSIS & OUTPUT": [
            st.Page("pages/6_MapReduce_Lab.py", title="MapReduce Lab", icon="⚙️"),
            st.Page("pages/7_Reports.py", title="Reports & Export", icon="📥"),
            st.Page("pages/8_About.py", title="About Project", icon="ℹ️"),
        ],
    }
)

with st.sidebar:
    st.markdown("### 📡 WebLog Analytics")
    st.caption("Big Data Analytics · Web server logs")
    st.divider()
    st.markdown("#### Data source")
    uploaded_file = st.file_uploader(
        "Upload Apache/Nginx access log",
        type=["log", "txt"],
        key="global_log_upload",
        help="Use a plain-text Apache/Nginx access log file.",
    )
    st.caption("No upload? The app uses data/access.log from your project folder.")
    top_n = st.slider("Top results to show", min_value=5, max_value=20, value=10, step=1)
    st.session_state["top_n"] = top_n

try:
    if uploaded_file is not None:
        raw_text = uploaded_file.getvalue().decode("utf-8", errors="replace")
        source_label = uploaded_file.name
    else:
        raw_text = load_default_text(ROOT / "data" / "access.log")
        source_label = "Included sample access.log"
except OSError as exc:
    st.error(f"Could not read the sample log file: {exc}")
    st.info("Check that the original project's data/access.log file is still present.")
    st.stop()

parsed_df, stats = parse_log_text(raw_text)
if parsed_df.empty:
    st.error("No valid Apache/Nginx log records were found in this file.")
    st.warning("Clear the uploaded file using the small ✕ in the uploader, then try the included sample log or a valid .log/.txt file.")
    st.caption("Expected example: 192.168.1.10 - - [28/Oct/2026:10:20:30 +0530] \"GET /home HTTP/1.1\" 200 1234")
    st.stop()

st.session_state["web_log_df"] = dataframe_for_app(parsed_df)
st.session_state["web_log_source"] = source_label
st.session_state["web_log_stats"] = stats

with st.sidebar:
    st.divider()
    st.markdown("#### Current dataset")
    st.metric("Valid requests", f"{len(parsed_df):,}")
    st.caption(f"{stats['parsed_lines']:,} valid / {stats['nonempty_lines']:,} non-empty lines")
    st.caption(f"Source: {source_label}")
    st.divider()
    st.caption("MapReduce is demonstrated locally in Python; Hadoop is not running in this app.")

nav.run()

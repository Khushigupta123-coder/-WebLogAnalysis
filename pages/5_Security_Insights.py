import pandas as pd
import streamlit as st

st.title("🛡️ Security Insights")
st.caption("Simple, explainable rules to prioritize log records for review. These indicators do not prove an attack.")
df = st.session_state["web_log_df"].copy()

all_ip = df.groupby("IP").agg(
    Requests=("IP", "size"),
    ErrorResponses=("Status", lambda s: int((s >= 400).sum())),
    ClientErrors=("Status", lambda s: int(((s >= 400) & (s < 500)).sum())),
    ServerErrors=("Status", lambda s: int((s >= 500).sum())),
).sort_values("Requests", ascending=False)
max_req = int(all_ip["Requests"].max()) if not all_ip.empty else 1
median_req = float(all_ip["Requests"].median()) if not all_ip.empty else 1.0
default_threshold = max(1, min(max_req, max(5, int(median_req * 3))))
threshold = st.slider("Flag IPs with at least this many requests", min_value=1, max_value=max(1, max_req), value=default_threshold)

flags = all_ip[(all_ip["Requests"] >= threshold) | (all_ip["ErrorResponses"] >= 3)].copy()
flags["Review reason"] = flags.apply(
    lambda row: "; ".join(reason for condition, reason in [
        (row["Requests"] >= threshold, f"High request volume (≥ {threshold})"),
        (row["ErrorResponses"] >= 3, "3 or more HTTP errors"),
    ] if condition), axis=1
)

c1, c2, c3 = st.columns(3)
c1.metric("Distinct IPs", f"{df['IP'].nunique():,}")
c2.metric("IPs meeting rules", f"{len(flags):,}")
c3.metric("4xx/5xx responses", f"{int((df['Status'] >= 400).sum()):,}")

st.markdown("#### Rule-based review queue")
if flags.empty:
    st.success("No IP addresses meet the current rule thresholds.")
else:
    st.dataframe(flags.reset_index().rename(columns={"IP": "IP address"}), use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download review queue CSV", flags.reset_index().to_csv(index=False).encode("utf-8"), "security_review_queue.csv", "text/csv")

st.markdown("#### Most active IP addresses")
st.dataframe(all_ip.head(15).reset_index(), use_container_width=True, hide_index=True)
st.warning("Interpretation limit: a busy IP or repeated error may be caused by normal users, bots, testing, shared networks, or misconfigured clients. This page is a rule-based triage aid, not an intrusion detector and not proof of malicious activity.")

# Web Log Analysis Using MapReduce Concepts
## Big Data Mini Project Report

**Student:** khushi gupta
**Roll number:** 31 
**Department:** Computer Engineering  
**College:** shree l r tiwari college of engineering and technology 
**Academic year:** 2026-2027

## 1. Abstract
Web servers produce access logs containing request timestamps, client IP addresses, requested paths, HTTP status codes and response sizes. This project parses access-log records and aggregates request counts to identify popular pages, common HTTP status codes, client activity and error requests. A Streamlit dashboard makes the analysis interactive. The starter implementation demonstrates mapper/reducer-style aggregation locally; it does not execute a Hadoop cluster.

## 2. Problem Statement
Large websites can generate many log records, making manual analysis inefficient. A structured aggregation process can summarize traffic patterns and help administrators identify popular resources and possible errors.

## 3. Objectives
- Read web-server access logs.
- Parse valid request records and ignore malformed lines.
- Count requests by page, status code, IP address and method.
- Summarize error responses and transferred bytes.
- Display charts and tables in an interactive dashboard.
- Explain how the MapReduce programming model can be used for log analysis.

## 4. Existing System
Manual inspection of raw text logs is slow and makes it difficult to compare traffic patterns across many records.

## 5. Proposed System
The proposed system parses log records into structured fields, maps each record to a key-value pair, aggregates counts by key, and presents the output through a dashboard.

## 6. Technologies
- Python: parsing and aggregation logic
- Streamlit: interactive web interface
- pandas: tabular data processing
- Matplotlib: charts
- Apache Hadoop MapReduce / Hadoop Streaming: discussed as the distributed execution model and optional extension

## 7. Dataset
The included `data/access.log` file contains synthetic Apache-style access log entries for demonstration. It is bundled with the project so no dataset download is needed. Do not describe the sample as real production traffic.

## 8. Methodology
1. Load lines from the sample log or a user-uploaded `.log`/`.txt` file.
2. Parse each line into IP, timestamp, method, page, HTTP status and response bytes.
3. Discard invalid records.
4. Map each chosen field to `(key, 1)`.
5. Reduce by summing values for each key.
6. Display request counts, status distribution, most requested pages and error totals.
7. Allow result tables to be downloaded as CSV.

## 9. System Architecture
**Access log → parser and validation → mapper (key, 1) → reducer (sum by key) → analytics dashboard**

## 10. Implementation
The application is implemented in `app.py`. The sidebar supports file upload and result-count selection. The Overview tab presents status-code and page charts. The MapReduce results tab lets the user select a field to aggregate. The Parsed records tab shows structured records and supports CSV export.

## 11. Results
The dashboard reports the number of valid requests, unique IP addresses, HTTP errors and transferred bytes. It visualizes HTTP status codes and the most requested pages. Actual screenshots should be inserted after running the application:
- Screenshot 1: Dashboard summary metrics
- Screenshot 2: HTTP status-code chart
- Screenshot 3: MapReduce aggregation table
- Screenshot 4: Parsed records table

## 12. Big Data Concepts and Limitations
MapReduce is a programming model in which mapping converts input records to intermediate key-value pairs and reducing combines values with the same key. This starter app demonstrates the idea on a local machine. It **does not run Hadoop or distributed processing**. If the course requires a genuine Big Data engine, execute the included mapper and reducer through Hadoop Streaming on a configured Hadoop installation, or ask whether a local MapReduce demonstration is acceptable.

## 13. Future Scope
- Run mapper and reducer scripts using Hadoop Streaming.
- Process a much larger log dataset.
- Add time-based traffic analysis and anomaly detection.
- Add daily/hourly traffic charts and automated error summaries.
- Deploy the dashboard for team access.

## 14. Conclusion
The project converts raw web-server logs into structured records and aggregates traffic metrics. It provides a practical, visual introduction to log analytics and the MapReduce programming model. The implementation scope must be described honestly during evaluation.

## 15. References
- Apache Hadoop documentation: https://hadoop.apache.org/docs/
- Streamlit documentation: https://docs.streamlit.io/
- pandas documentation: https://pandas.pydata.org/docs/
